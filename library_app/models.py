from django.db import models


class LibraryRecord(models.Model):
    """
    Tracks a student's library standing — fines and borrowed books.
    Integration Pattern: Message - data entity exchanged between Library
    spoke and the Integration Hub.
    """
    student_id = models.CharField(max_length=10)
    has_fines = models.BooleanField(default=False)
    amount_due = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    books_borrowed = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['student_id']

    def __str__(self):
        status = "with fines" if self.has_fines else "clear"
        return f"LibraryRecord [{self.student_id}] - {status}"
