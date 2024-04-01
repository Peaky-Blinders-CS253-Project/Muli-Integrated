"""
URL configuration for messautomation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# messautomation/urls.py

from django.contrib import admin
from django.urls import include, path
from .views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mess-manager-login', home, name='home'),
    path('mess-manager/', include('mess_manager.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('students/', include('students.urls')),
    path('gate-watcher/', include('gate_watcher.urls')),
    path('extra-meal-booking/', include('extra_meal_booking.urls')),
    path('extra-meal-giving/', include('extra_meal_giving.urls')),
   
    # Add other app-specific URL includes
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

