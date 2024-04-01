# mess/admin.py

from django.contrib import admin
from .models import Student, Worker, Meal, Booking, BaseMealCharge, DailyBreakdown

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'name', 'base_meal_charge_due')
    search_fields = ('roll_number', 'name')

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'role')

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_charge')
    search_fields = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('student', 'meal', 'booking_date', 'is_extra', 'is_cancelled', 'hash_number', 'is_given')
    list_filter = ('is_extra', 'is_cancelled', 'is_given')
    search_fields = ('student__roll_number', 'meal__name', 'hash_number')

@admin.register(BaseMealCharge)
class BaseMealChargeAdmin(admin.ModelAdmin):
    list_display = ('meal', 'base_charge', 'date')
    search_fields = ('meal__name', 'date')

@admin.register(DailyBreakdown)
class DailyBreakdownAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'booked_meals_count')
    search_fields = ('student__roll_number', 'date')
