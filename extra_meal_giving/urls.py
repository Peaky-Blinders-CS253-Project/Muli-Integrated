from django.urls import path
from .views import ExtrasGivingStatusView

urlpatterns = [
    path('extras_giving_status/<str:roll_number>/', ExtrasGivingStatusView.as_view(), name='extras_giving_status'),
    # Add other URL patterns as needed
]
