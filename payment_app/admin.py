from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'payment_type', 'amount_paid', 'status', 'reference_number', 'date_paid']
    list_filter = ['status', 'payment_type']
    search_fields = ['student_id', 'reference_number']
    ordering = ['-date_paid']
