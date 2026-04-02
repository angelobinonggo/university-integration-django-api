"""
Library App Views
-----------------
Integration Pattern: Request-Response
This ViewSet exposes CRUD endpoints for LibraryRecord.
The Integration Hub calls these endpoints to check a student's library standing.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import LibraryRecord
from .serializers import LibraryRecordSerializer


class LibraryRecordViewSet(viewsets.ModelViewSet):
    """
    A ViewSet providing CRUD operations for LibraryRecord.

    Endpoints:
        GET    /api/library/                    - List all records
        POST   /api/library/                    - Create a record
        GET    /api/library/{id}/               - Retrieve a record
        PUT    /api/library/{id}/               - Full update
        PATCH  /api/library/{id}/               - Partial update
        DELETE /api/library/{id}/               - Delete
        GET    /api/library/by_student_id/      - Lookup by student_id field
    """
    queryset = LibraryRecord.objects.all()
    serializer_class = LibraryRecordSerializer

    @action(detail=False, methods=['get'], url_path='by_student_id')
    def by_student_id(self, request):
        """
        Message Routing Pattern:
        Hub uses this to route a library-status request to the correct record.
        """
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id query parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            record = LibraryRecord.objects.get(student_id=student_id)
            serializer = LibraryRecordSerializer(record)
            return Response(serializer.data)
        except LibraryRecord.DoesNotExist:
            return Response(
                {'error': f'No library record found for student_id "{student_id}".'},
                status=status.HTTP_404_NOT_FOUND
            )
