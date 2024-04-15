from django.db import models
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import AbstractUser,  Group
# students/models.py
# students/models.py

from django.db import models



class Student(AbstractUser):
    rollno = models.IntegerField(default=0,unique=True)
    username = models.CharField(max_length=255,unique=True)
    email = models.EmailField(max_length=254)
    paid_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)
    is_student = models.BooleanField(default=True)
    # Specify custom related_name for groups and user_permissions
    groups = models.ManyToManyField(Group, related_name='student_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='student_permissions')


    def __str__(self):
        return self.username


class ExtraItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Date = models.DateField( auto_now=False, auto_now_add=False,null= True)
    Time = models.TextField(max_length=15,null=True)
    Day = models.CharField(max_length=15,null=True)
    Type= models.TextField(max_length=15,default='Regular')

class BookingExtraItems(models.Model):
    rollno = models.IntegerField(default=0)
    date = models.DateField()
    time = models.CharField(max_length=20,default= 'Breakfast')
    extra_item = models.CharField(max_length=50,default='DCBM')    

class BreakdownChart(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    base_meal_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_extras_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
class BreakdownChartExtra(models.Model):
    breakdown_chart = models.ForeignKey(BreakdownChart, on_delete=models.CASCADE, related_name='extras')
    extra_item = models.ForeignKey(BookingExtraItems, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
# class Student(models.Model):
#        username = models.CharField(max_length=255, unique=True)
#     name = models.CharField(max_length=255)
#     paid_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     remaining_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class BaseMealPrecancellation(models.Model):
    rollno = models.IntegerField(default=0)
    date = models.DateField()
    time = models.CharField(max_length=20,default= 'Breakfast')


    # Add other fields for extra items


