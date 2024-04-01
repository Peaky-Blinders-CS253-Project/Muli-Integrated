# authentication.py

from django.contrib.auth.backends import ModelBackend
from .models import Student

class RollNumberBackend(ModelBackend):
    def authenticate(self, request, rollno=None, password=None, **kwargs):
        try:
            user = Student.objects.get(rollno=rollno)
            if user.check_password(password):
                return user
        except Student.DoesNotExist:
            return None
