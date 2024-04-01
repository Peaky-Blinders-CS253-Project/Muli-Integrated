# gate_watcher/views.py
from django.shortcuts import render
from django.views import View

class GateStaffView(View):
    def get(self, request):
        # Your logic for handling GET requests
        return render(request, 'gate_watcher/gate_staff.html', context={'message': 'Welcome, Gate Staff!'})

    def post(self, request):
        # Your logic for handling POST requests
        # You can access form data using request.POST
        return render(request, 'gate_watcher/gate_staff.html', context={'message': 'Form submitted successfully!'})