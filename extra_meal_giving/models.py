from django.db import models
from students.models import Student

class ExtraMealGiving(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    hash_number = models.CharField(max_length=50, unique=True)
    # Add other fields for extra meal giving details

    def __str__(self):
        return f"{self.student.name} - {self.date}"

    # Add any other fields or methods as needed
