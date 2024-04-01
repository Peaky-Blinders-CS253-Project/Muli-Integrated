from django.shortcuts import render
from .models import ExtraMealGiving
from django.views import View 
from students.models import Student

class ExtrasGivingStatusView(View):
    def get(self, request, roll_number):
        student = Student.objects.get(roll_number=roll_number)
        extras_givings = ExtraMealGiving.objects.filter(student=student)
        return render(request, 'extra_meal_giving/extras_giving_status.html', {'student': student, 'extras_givings': extras_givings})
