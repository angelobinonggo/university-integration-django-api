from django.contrib import admin
from .models import LibraryRecord


@admin.register(LibraryRecord)
class LibraryRecordAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'has_fines', 'amount_due', 'books_borrowed', 'last_updated']
    list_filter = ['has_fines']
    search_fields = ['student_id']
    ordering = ['student_id']
