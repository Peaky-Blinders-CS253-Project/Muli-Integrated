from django.urls import path
from .views import extra_meal_menu

urlpatterns = [
    path('extra_meal_menu/', extra_meal_menu, name='extra_meal_menu'),
   
    # Add other URL patterns as needed
]
