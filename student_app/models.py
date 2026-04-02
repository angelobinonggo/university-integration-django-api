from django.db import models


class Student(models.Model):
    """
    Represents a student in the university system.
    Integration Pattern: Message - this is the core entity/payload
    shared across all spoke systems.
    """
    student_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=50)
    email = models.EmailField()
    year_level = models.PositiveSmallIntegerField(default=1)
    is_enrolled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['student_id']

    def __str__(self):
        return f"{self.student_id} - {self.name}"
