from django.contrib import admin
from .models import Student
from .models import BreakdownChart, BreakdownChartExtra,ExtraItem,BaseMealPrecancellation
@admin.register(BreakdownChart)
class BreakdownChartAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'date', 'base_meal_price', 'total_extras_price', 'total_cost')
    list_filter = ('student', 'date')
    search_fields = ('student__username', 'date')

@admin.register(BreakdownChartExtra)
class BreakdownChartExtraAdmin(admin.ModelAdmin):
    list_display = ('id', 'breakdown_chart', 'extra_item', 'quantity', 'price')
    list_filter = ('breakdown_chart__student', 'extra_item')
    search_fields = ('breakdown_chart__student__username', 'extra_item__name')

from .models import BookingExtraItems

class BookingExtraItemsAdmin(admin.ModelAdmin):
    list_display = ('rollno', 'date', 'time', 'extra_item')
    search_fields = ('rollno', 'extra_item')
    list_filter = ('date', 'time')

admin.site.register(BookingExtraItems, BookingExtraItemsAdmin)


class BaseMealPrecancellationAdmin(admin.ModelAdmin):
    list_display = ['rollno', 'date', 'time']  # Fields to display in the admin list view

# Register the BaseMealPrecancellation model with the admin site
admin.site.register(BaseMealPrecancellation, BaseMealPrecancellationAdmin)




class StudentAdmin(admin.ModelAdmin):
    list_display = ('rollno', 'password', 'username', 'paid_fees', 'email', 'is_superuser','is_student')
    list_filter = ('is_superuser',)  # Optionally, you can add filters
    search_fields = ('username', 'name')  # Optionally, you can add search fields

# Register the Student model with the custom admin class
admin.site.register(Student, StudentAdmin)


class ExtraItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price','Date','Time','Day','Type']  # Define which fields to display in the list view
    search_fields = ['name','Date','Day']  # Add fields you want to be searchable in the admin interface

admin.site.register(ExtraItem, ExtraItemAdmin)