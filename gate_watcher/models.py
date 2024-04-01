# gate_watcher/models.py

from django.db import models

class GateWatcher(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)  # You should use a more secure way to store passwords in a real application

    def __str__(self):
        return self.username

    # Add any other fields or methods as needed
