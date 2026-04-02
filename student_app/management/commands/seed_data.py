"""
Management command to seed sample data for the University Integration Platform.
Run with: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from student_app.models import Student
from library_app.models import LibraryRecord
from payment_app.models import Payment


STUDENTS = [
    {'student_id': 'S001', 'name': 'Juan dela Cruz', 'course': 'BS Information Technology', 'email': 'juan@uni.edu.ph', 'year_level': 3, 'is_enrolled': True},
    {'student_id': 'S002', 'name': 'Maria Santos', 'course': 'BS Computer Science', 'email': 'maria@uni.edu.ph', 'year_level': 2, 'is_enrolled': True},
    {'student_id': 'S003', 'name': 'Pedro Reyes', 'course': 'BS Information Systems', 'email': 'pedro@uni.edu.ph', 'year_level': 4, 'is_enrolled': True},
    {'student_id': 'S004', 'name': 'Ana Garcia', 'course': 'BS Computer Engineering', 'email': 'ana@uni.edu.ph', 'year_level': 1, 'is_enrolled': False},
]

LIBRARY_RECORDS = [
    {'student_id': 'S001', 'has_fines': False, 'amount_due': 0.00, 'books_borrowed': 2},
    {'student_id': 'S002', 'has_fines': True, 'amount_due': 150.00, 'books_borrowed': 1},
    {'student_id': 'S003', 'has_fines': False, 'amount_due': 0.00, 'books_borrowed': 0},
    # S004 has no library record
]

PAYMENTS = [
    {'student_id': 'S001', 'payment_type': 'TUITION', 'amount_paid': 15000.00, 'status': 'PAID', 'reference_number': 'PAY-2025-0001', 'remarks': 'First semester tuition'},
    {'student_id': 'S001', 'payment_type': 'MISC', 'amount_paid': 500.00, 'status': 'PAID', 'reference_number': 'PAY-2025-0002', 'remarks': 'Miscellaneous fee'},
    {'student_id': 'S002', 'payment_type': 'TUITION', 'amount_paid': 15000.00, 'status': 'PAID', 'reference_number': 'PAY-2025-0003', 'remarks': 'First semester tuition'},
    {'student_id': 'S003', 'payment_type': 'TUITION', 'amount_paid': 10000.00, 'status': 'PENDING', 'reference_number': 'PAY-2025-0004', 'remarks': 'Partial tuition payment'},
    # S004 has no payment
]


class Command(BaseCommand):
    help = 'Seeds the database with sample data for the University Integration Platform.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Seeding sample data...'))

        # Clear existing
        Student.objects.all().delete()
        LibraryRecord.objects.all().delete()
        Payment.objects.all().delete()

        for data in STUDENTS:
            Student.objects.create(**data)
        self.stdout.write(self.style.SUCCESS(f'  Created {len(STUDENTS)} students.'))

        for data in LIBRARY_RECORDS:
            LibraryRecord.objects.create(**data)
        self.stdout.write(self.style.SUCCESS(f'  Created {len(LIBRARY_RECORDS)} library records.'))

        for data in PAYMENTS:
            Payment.objects.create(**data)
        self.stdout.write(self.style.SUCCESS(f'  Created {len(PAYMENTS)} payment records.'))

        self.stdout.write(self.style.SUCCESS('\nSeed complete! Try:'))
        self.stdout.write('  GET /api/hub/student-summary/?student_id=S001')
        self.stdout.write('  GET /api/hub/all-summaries/')
        self.stdout.write('  GET /api/hub/health/')
