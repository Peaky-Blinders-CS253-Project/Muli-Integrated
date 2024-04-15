# mess_manager/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models




class ManagerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_manager=True)

class Manager(AbstractUser):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    groups = models.ManyToManyField(Group, related_name='manager_groups')  # Change related_name
    user_permissions = models.ManyToManyField(Permission, related_name='manager_permissions')  # Change related_name
    is_manager = models.BooleanField(default=True)

    objects = ManagerManager()


class FoodItem(models.Model):
    name = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.name


class MessMenu(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    day = models.CharField(max_length=255, choices=DAY_CHOICES)
    breakfast = models.CharField( max_length=150)
    lunch = models.CharField( max_length=150)
    dinner = models.CharField( max_length=150)

    def __str__(self):
        return f"{self.day} - Breakfast: {self.breakfast.name}, Lunch: {self.lunch.name}, Dinner: {self.dinner.name} - Price: {self.price}"


  
class Meal(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    BREAKFAST = 'Breakfast'
    LUNCH = 'Lunch'
    DINNER = 'Dinner'

    MEAL_CHOICES = [
        (BREAKFAST, 'Breakfast'),
        (LUNCH, 'Lunch'),
        (DINNER, 'Dinner'),
    ]

    day = models.CharField(max_length=255, choices=DAY_CHOICES)
    meal_type = models.CharField(max_length=255, choices=MEAL_CHOICES)
    item_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.day} - {self.meal_type} - {self.item_name}"


class WorkerStaff(models.Model):
    # Model for worker staff, storing their login credentials
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

class BaseMealCharge(models.Model):
    # Model for base meal charges, storing charges for each meal each day
    date = models.DateField()
    charge = models.DecimalField(max_digits=10, decimal_places=2)
    min_charge = models.DecimalField(max_digits=10,decimal_places=2,default=0)

