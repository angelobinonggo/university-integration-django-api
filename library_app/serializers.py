from rest_framework import serializers
from .models import LibraryRecord


class LibraryRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for LibraryRecord.
    Data Transformation Pattern: standardizes library data for
    cross-system exchange via the Integration Hub.
    """
    library_status = serializers.SerializerMethodField()

    class Meta:
        model = LibraryRecord
        fields = [
            'id', 'student_id', 'has_fines', 'amount_due',
            'books_borrowed', 'library_status', 'last_updated'
        ]
        read_only_fields = ['id', 'last_updated', 'library_status']

    def get_library_status(self, obj):
        if obj.has_fines:
            return f"HOLD - Unpaid fine of ₱{obj.amount_due}"
        return "CLEAR"
