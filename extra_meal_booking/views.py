from django.shortcuts import render, redirect
from django.views import View
from .models import ExtraMealMenu
from .forms import BookExtraMealForm
from django.contrib.auth.decorators import login_required

@login_required
def extra_meal_menu(request):
    extra_meals = ExtraMealMenu.objects.all()
    return render(request, 'extra_meal_booking/extra_meal_menu.html', {'extra_meals': extra_meals})



