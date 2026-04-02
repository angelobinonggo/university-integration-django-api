from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'course', 'year_level', 'is_enrolled', 'created_at']
    list_filter = ['course', 'year_level', 'is_enrolled']
    search_fields = ['student_id', 'name', 'email']
    ordering = ['student_id']
