from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Student model.
    Data Transformation Pattern: converts Python model instance
    to/from JSON for API communication.
    """
    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'name', 'course',
            'email', 'year_level', 'is_enrolled', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class StudentSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer used by the Integration Hub."""
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'course', 'year_level', 'is_enrolled']
