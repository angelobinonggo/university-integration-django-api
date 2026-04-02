"""
Payment App Views
-----------------
Integration Pattern: Request-Response
This ViewSet exposes CRUD endpoints for Payment records.
The Integration Hub calls these endpoints to retrieve payment history.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer, PaymentSummarySerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    A ViewSet providing CRUD operations for Payment records.

    Endpoints:
        GET    /api/payments/                  - List all payments
        POST   /api/payments/                  - Record a new payment
        GET    /api/payments/{id}/             - Retrieve a payment
        PUT    /api/payments/{id}/             - Full update
        PATCH  /api/payments/{id}/             - Partial update
        DELETE /api/payments/{id}/             - Delete
        GET    /api/payments/by_student_id/    - List payments by student_id
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=['get'], url_path='by_student_id')
    def by_student_id(self, request):
        """
        Message Routing Pattern:
        Hub routes payment-history queries here using the student_id field.
        """
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id query parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        payments = Payment.objects.filter(student_id=student_id)
        serializer = PaymentSummarySerializer(payments, many=True)
        total = sum(p.amount_paid for p in payments if p.status == 'PAID')
        return Response({
            'student_id': student_id,
            'total_paid': float(total),
            'payment_count': payments.count(),
            'payments': serializer.data,
        })
