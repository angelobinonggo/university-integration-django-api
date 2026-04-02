from django.db import models


class Payment(models.Model):
    """
    Records tuition and other payments made by a student.
    Integration Pattern: Message - payment data routed through the Hub
    for consolidated reporting.
    """

    PAYMENT_TYPE_CHOICES = [
        ('TUITION', 'Tuition Fee'),
        ('MISC', 'Miscellaneous Fee'),
        ('LIBRARY', 'Library Fine'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('PENDING', 'Pending'),
        ('FAILED', 'Failed'),
    ]

    student_id = models.CharField(max_length=10)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES, default='TUITION')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PAID')
    reference_number = models.CharField(max_length=30, unique=True)
    date_paid = models.DateField(auto_now_add=True)
    remarks = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-date_paid']

    def __str__(self):
        return f"Payment [{self.student_id}] - ₱{self.amount_paid} ({self.status})"
