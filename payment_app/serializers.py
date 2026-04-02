from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payment model.
    Data Transformation Pattern: normalizes payment data for
    routing through Integration Hub.
    """
    class Meta:
        model = Payment
        fields = [
            'id', 'student_id', 'payment_type', 'amount_paid',
            'status', 'reference_number', 'date_paid', 'remarks'
        ]
        read_only_fields = ['id', 'date_paid']


class PaymentSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer used by the Integration Hub."""
    class Meta:
        model = Payment
        fields = ['payment_type', 'amount_paid', 'status', 'reference_number', 'date_paid']
