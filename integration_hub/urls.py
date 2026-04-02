"""
Integration Hub URL Configuration
===================================
Central hub endpoints — these aggregate and route across all spokes.

Pattern: Hub-and-Spoke
  /api/hub/health/           — Spoke health/status monitor
  /api/hub/student-summary/  — Unified student report (Request-Response + Transformation)
  /api/hub/all-summaries/    — All-student report (Aggregator pattern)
"""

from django.urls import path
from .views import StudentSummaryView, AllStudentSummariesView, HubHealthView

urlpatterns = [
    path('hub/health/', HubHealthView.as_view(), name='hub-health'),
    path('hub/student-summary/', StudentSummaryView.as_view(), name='hub-student-summary'),
    path('hub/all-summaries/', AllStudentSummariesView.as_view(), name='hub-all-summaries'),
]
