"""
Integration Hub Views
=====================
This is the CENTRAL HUB of the Hub-and-Spoke Architecture.

Integration Patterns applied here:
  1. Request-Response Pattern  — Hub requests data from each spoke system.
  2. Message Routing Pattern   — Hub routes API calls to the correct spoke.
  3. Data Transformation Pattern — Hub aggregates and standardizes JSON
                                    responses from all spokes into a unified
                                    student summary payload.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from student_app.models import Student
from student_app.serializers import StudentSerializer
from library_app.models import LibraryRecord
from library_app.serializers import LibraryRecordSerializer
from payment_app.models import Payment
from payment_app.serializers import PaymentSummarySerializer


# ---------------------------------------------------------------------------
# Helper: Message Router
# ---------------------------------------------------------------------------

def _route_to_student(student_id: str):
    """
    Message Routing Pattern:
    Routes the request to the Student spoke and returns the student object
    or None if not found.
    """
    try:
        return Student.objects.get(student_id=student_id), None
    except Student.DoesNotExist:
        return None, f'Student with ID "{student_id}" not found in the Student system.'


def _route_to_library(student_id: str):
    """
    Message Routing Pattern:
    Routes the request to the Library spoke and returns the library record
    or a default "no record" dict.
    """
    try:
        record = LibraryRecord.objects.get(student_id=student_id)
        return LibraryRecordSerializer(record).data
    except LibraryRecord.DoesNotExist:
        return {
            'student_id': student_id,
            'has_fines': False,
            'amount_due': '0.00',
            'books_borrowed': 0,
            'library_status': 'NO RECORD FOUND',
        }


def _route_to_payment(student_id: str):
    """
    Message Routing Pattern:
    Routes the request to the Payment spoke and returns aggregated payment data.
    """
    payments = Payment.objects.filter(student_id=student_id)
    total_paid = sum(p.amount_paid for p in payments if p.status == 'PAID')
    serialized = PaymentSummarySerializer(payments, many=True).data
    return {
        'student_id': student_id,
        'total_paid': float(total_paid),
        'payment_count': payments.count(),
        'payments': serialized,
    }


# ---------------------------------------------------------------------------
# Hub Views
# ---------------------------------------------------------------------------

class StudentSummaryView(APIView):
    """
    GET /api/hub/student-summary/?student_id=<id>

    Hub-and-Spoke: Central hub that aggregates data from all three spokes:
      - Student App  → profile information
      - Library App  → library standing & fines
      - Payment App  → tuition payment history

    Data Transformation Pattern:
    The hub normalizes the three separate JSON payloads into a single,
    unified response structure.
    """

    def get(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {
                    'error': 'student_id query parameter is required.',
                    'usage': '/api/hub/student-summary/?student_id=S001',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ── Step 1: Route to Student Spoke ──────────────────────────────────
        student, err = _route_to_student(student_id)
        if err:
            return Response({'error': err}, status=status.HTTP_404_NOT_FOUND)

        # ── Step 2: Route to Library Spoke ──────────────────────────────────
        library_data = _route_to_library(student_id)

        # ── Step 3: Route to Payment Spoke ──────────────────────────────────
        payment_data = _route_to_payment(student_id)

        # ── Step 4: Data Transformation — build unified response ────────────
        unified_response = {
            'integration_pattern': 'Hub-and-Spoke | Request-Response | Data Transformation',
            'hub': 'University Integration Platform',
            'student_profile': StudentSerializer(student).data,
            'library_standing': library_data,
            'payment_summary': payment_data,
            'clearance_status': _compute_clearance(library_data, payment_data),
        }

        return Response(unified_response, status=status.HTTP_200_OK)


class AllStudentSummariesView(APIView):
    """
    GET /api/hub/all-summaries/

    Aggregator Pattern:
    Returns consolidated summaries for ALL students in the system.
    The hub iterates over each student, routes requests to all spokes,
    and combines the results into one response.
    """

    def get(self, request):
        students = Student.objects.all()
        summaries = []

        for student in students:
            sid = student.student_id
            library_data = _route_to_library(sid)
            payment_data = _route_to_payment(sid)
            summaries.append({
                'student_id': sid,
                'name': student.name,
                'course': student.course,
                'year_level': student.year_level,
                'is_enrolled': student.is_enrolled,
                'library_status': library_data.get('library_status', 'UNKNOWN'),
                'total_paid': payment_data['total_paid'],
                'clearance_status': _compute_clearance(library_data, payment_data),
            })

        return Response({
            'integration_pattern': 'Hub-and-Spoke | Aggregator',
            'hub': 'University Integration Platform',
            'total_students': len(summaries),
            'summaries': summaries,
        })


class HubHealthView(APIView):
    """
    GET /api/hub/health/

    Returns a health/status report of all spokes accessible by the hub.
    Useful for monitoring the integration architecture.
    """

    def get(self, request):
        student_count = Student.objects.count()
        library_count = LibraryRecord.objects.count()
        payment_count = Payment.objects.count()

        return Response({
            'hub': 'University Integration Platform',
            'architecture': 'Hub-and-Spoke',
            'status': 'OPERATIONAL',
            'spokes': {
                'student_app': {
                    'status': 'CONNECTED',
                    'endpoint': '/api/students/',
                    'records': student_count,
                },
                'library_app': {
                    'status': 'CONNECTED',
                    'endpoint': '/api/library/',
                    'records': library_count,
                },
                'payment_app': {
                    'status': 'CONNECTED',
                    'endpoint': '/api/payments/',
                    'records': payment_count,
                },
            },
            'integration_patterns': [
                'Request-Response',
                'Message Routing',
                'Data Transformation',
                'Aggregator',
            ],
        })


# ---------------------------------------------------------------------------
# Helper: Compute Clearance
# ---------------------------------------------------------------------------

def _compute_clearance(library_data: dict, payment_data: dict) -> dict:
    """
    Data Transformation Pattern:
    Combines data from multiple spokes to derive a clearance decision.
    This is a simple business rule engine running inside the hub.
    """
    issues = []

    has_fines = library_data.get('has_fines', False)
    if has_fines:
        amount = library_data.get('amount_due', 0)
        issues.append(f'Library fine of ₱{amount} unpaid.')

    if payment_data['payment_count'] == 0:
        issues.append('No tuition payment on record.')

    cleared = len(issues) == 0
    return {
        'cleared': cleared,
        'status': 'CLEARED' if cleared else 'NOT CLEARED',
        'issues': issues,
    }
