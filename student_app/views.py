"""
Student App Views
-----------------
Integration Pattern: Request-Response
This ViewSet exposes CRUD endpoints for the Student model.
The Integration Hub calls these endpoints to retrieve student data.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Student
from .serializers import StudentSerializer, StudentSummarySerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    A ViewSet providing CRUD operations for Student records.

    Endpoints (routed by DefaultRouter):
        GET    /api/students/               - List all students
        POST   /api/students/               - Create a new student
        GET    /api/students/{id}/          - Retrieve a student
        PUT    /api/students/{id}/          - Update a student (full)
        PATCH  /api/students/{id}/          - Update a student (partial)
        DELETE /api/students/{id}/          - Delete a student
        GET    /api/students/by_student_id/ - Lookup by student_id field
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=False, methods=['get'], url_path='by_student_id')
    def by_student_id(self, request):
        """
        Message Routing Pattern:
        Allows the hub to query a student by their string student_id
        rather than the database primary key.
        """
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id query parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            student = Student.objects.get(student_id=student_id)
            serializer = StudentSummarySerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response(
                {'error': f'Student with student_id "{student_id}" not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
