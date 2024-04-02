# mess_manager/forms.py
from django import forms
from .models import MessMenu, Meal
from students.models import Student,ExtraItem
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from django.core.exceptions import ValidationError
class BaseMealChargeForm(forms.Form):
    date = forms.DateField()
    base_meal_charge = forms.DecimalField(max_digits=10, decimal_places=2)

class ManagerLoginForm(AuthenticationForm):
    pass  # Use Django's built-in AuthenticationForm






class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['day', 'meal_type', 'item_name', 'price']


class AddWorkerStaffForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

class MessMenuForm(forms.ModelForm):
    breakfast =forms.CharField(max_length=100)
    lunch = forms.CharField(max_length=100)
    dinner = forms.CharField(max_length=100)
    
    class Meta:
        model = MessMenu
        fields = ['day', 'breakfast', 'lunch', 'dinner']

#class ExtraMealMenuForm(forms.ModelForm):
#    class Meta:
 ##       model = ExtraMealMenu
 #       fields = ['item_name', 'price', 'date', 'time']
# class BaseMealChargeForm(forms.ModelForm):
#     class Meta:
#         model = BaseMealCharge
#         fields = ['day', 'charge']