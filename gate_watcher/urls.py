# gate_watcher/urls.py

from django.urls import path
from .views import GateStaffView

urlpatterns = [
    path('gate-staff/<str:roll_number>/', GateStaffView.as_view(), name='gate_staff'),
    # Add other URLs for gate watcher views
]
