# students/forms.py

from django import forms
from .models import BaseMealPrecancellation, BookingExtraItems
from .models import Student
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
class StudentRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
  
class StudentLoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

#class BaseMealPrecancellationForm(forms.ModelForm):
  #  class Meta:
  #      model = BaseMealPrecancellation
   #     fields = ['student', 'date', 'time']
        # Add other fields as needed
        # Example: fields = ['student', 'date', 'is_precancelled', 'additional_field']


class StudentCardForm(forms.Form):
    # Define fields for the StudentCardForm if needed
    # Example: roll_number = forms.CharField(max_length=10)
    pass
class StudentLoginForm(forms.Form):
    roll_no = forms.IntegerField(label='Roll No.')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)