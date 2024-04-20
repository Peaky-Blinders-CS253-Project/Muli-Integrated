from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from .models import MessMenu, Manager, FoodItem
from .forms import  AddWorkerStaffForm,MessMenuForm, ManagerLoginForm, BaseMealChargeForm
from students.models import Student,BaseMealPrecancellation,BookingExtraItems
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import check_password
from django.views.generic import FormView
from random import choice
from django.utils import timezone
from datetime import datetime, timedelta
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from students.models import ExtraItem
from students.models import BreakdownChart
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group
from django.views import View
from django.shortcuts import render, redirect  # Import your AddStudentForm here
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.utils import timezone
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from datetime import datetime
from django.core.mail import send_mail


from .models import BaseMealCharge
class BaseMealChargeView(View):
    template_name = 'mess_manager/set_base_meal_charge.html'

    def get(self, request):
        form = BaseMealChargeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BaseMealChargeForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            base_meal_charge = form.cleaned_data['base_meal_charge']
            min_charge = form.cleaned_data['min_charge']
            
            BaseMealCharge.objects.create(date=date, charge=base_meal_charge , min_charge=min_charge)
            return redirect('base_meal_charge_success')  # Redirect to a success page

        return render(request, self.template_name, {'form': form})





class BaseMealChargeSuccessView(View):
    def get(self, request):
        # Your success view logic here
        return render(request, 'mess_manager/base_meal_charge_success.html')  

 








def update_price(request, extra_id):
    if not request.user.is_authenticated or request.user.is_student:
            return HttpResponseForbidden("You don't have permission to perform this action.")
    extra_item = get_object_or_404(ExtraItem, pk=extra_id)
    if request.method == 'POST':
        new_price = request.POST.get('price')
        extra_item.price = new_price
        extra_item.save()
        messages.success(request, 'Price updated successfully.')
        return redirect('extraitemcreate')
    return redirect('extraitemcreate')




class ExtraItemList(ListView):
    template_name = 'mess_manager/extra_meal_menu.html'

    def get_queryset(self):
        return ExtraItem.objects.all()  # Provide the queryset of extra items

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.is_student:
            return HttpResponseForbidden("You don't have permission to access this page.")
        return render(request, self.template_name, {'object_list': self.get_queryset()})

class ExtraItemUpdate(UpdateView):
    model = ExtraItem
    fields = ['name', 'price']
    template_name = 'mess_manager/extra_item_form.html'  # Use the same template as ExtraItemCreate
    success_url = reverse_lazy('extraitem_list')

    def form_valid(self, form):
        if not self.request.user.is_authenticated or self.request.user.is_student:
            return HttpResponseForbidden("You don't have permission to perform this action.")
        return super().form_valid(form)


def ExtraItemCreate(request):
    if not request.user.is_authenticated or request.user.is_student:
        return HttpResponseForbidden("You don't have permission to perform this action.")

    if request.method == "POST":
        Type = request.POST.get('Type')
        name = request.POST.get('name')
        price = request.POST.get('price')
        Date = request.POST.get('Date')
        Day = request.POST.get('Day')
        Time = request.POST.get('Time')

        # Applying conditions based on the selected type
        if Type == 'regular':
            Date = None
            Time = None
            Day = None
        elif Type == 'weekly':
            Date = None
        elif Type == 'special':
            Day = None

        # Validating that the chosen date is greater than today's date
        if Date:
            chosen_date = datetime.strptime(Date, '%Y-%m-%d').date()
            if chosen_date <= timezone.now().date():
                message = 'Date should be greater than today'
                extras = ExtraItem.objects.all()
                return render(request, 'mess_manager/extra_meal_menu.html', {'message': message, 'extras': extras})

        # Create the ExtraItem object
        extra_item = ExtraItem.objects.create(
            Type=Type,
            name=name,
            price=price,
            Date=Date,
            Day=Day,
            Time=Time
        )

        # You can redirect to a success URL or render a template here
        message = 'Extras/Juice added successfully'
        extras = ExtraItem.objects.all()
        return render(request, 'mess_manager/extra_meal_menu.html', {'message': message, 'extras': extras})

    # Handle GET requests
    extras = ExtraItem.objects.all()
    return render(request, 'mess_manager/extra_meal_menu.html', {'extras': extras})

class ExtraItemDelete(DeleteView):
    model = ExtraItem
    template_name = 'mess_manager/extraitem_confirm_delete.html'
    success_url = reverse_lazy('extraitem_list')

    def delete(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated or self.request.user.is_student:
            return HttpResponseForbidden("You don't have permission to perform this action.")
        return super().delete(request, *args, **kwargs)

def delete_extra_item(request, item_id):
    if not request.user.is_authenticated or request.user.is_student:
            return HttpResponseForbidden("You don't have permission to perform this action.")
    if request.method == 'POST':
        extra_item = get_object_or_404(ExtraItem, pk=item_id)
        extra_item.delete()
        messages.success(request, 'Extra item deleted successfully.')
    return redirect('extraitemcreate')  # Redirect to the page where extra items are managed









class ManagerLoginView(View):
    def get(self, request):
        return render(request, 'mess_manager/manager_login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.username == 'manager':
            login(request, user)
            return redirect(reverse('manager_dashboard'))
        else:
            return render(request, 'mess_manager/manager_login.html', {'error': 'Invalid username or password'})
        

class ManagerDashboardView(View):
    template_name = 'mess_manager/manager_dashboard.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.is_student:
            # Assuming 'is_student' is the attribute indicating if the user is a student
            return HttpResponseForbidden("You don't have permission to access this page.")
        
        # Add any additional logic needed for the manager dashboard
        return render(request, self.template_name)


def AddStudentView(request):
    if not request.user.is_authenticated or request.user.is_student:
            return HttpResponseForbidden("You don't have permission to perform this action.")
    if request.method == "POST":
        name = request.POST.get('name')
        rollno = request.POST.get('rollno')
        email = request.POST.get('email')
        password = request.POST.get('password')
        hashed_password = make_password(password)
        if Student.objects.filter(rollno=rollno).exists():
            message = "Roll number already exists."
            return render(request, 'mess_manager/add_student.html',{'message':message})
        try:
            student_group = Group.objects.get(name='Students')
        except ObjectDoesNotExist:
            # Handle the case when the 'Students' group does not exist
            # For example, you can create the group here or handle it based on your application's requirements
            # Here, we'll create the group if it doesn't exist
            student_group = Group.objects.create(name='Students')

        en = Student(username=name, rollno=rollno, email=email, password=hashed_password)
        en.save()
        
        # Add the student to the 'Students' group
        en.groups.add(student_group)
        send_mail(
        'Welcome to Muli',  # Subject
        f'Your password to login in Muli is: {password}',  # Message body with password
        'mulitesting@gmail.com',  # Sender's email address
        [email],  # List of recipient email addresses
        fail_silently=False
        )
        
        return redirect('add_student_success') 
    
    return render(request, 'mess_manager/add_student.html')


class AddStudentSuccessView(View):
    def get(self, request):
        # Your success view logic here
        return render(request, 'mess_manager/addstudentsuccessful.html')  






class UpdateMessMenuView(View):
    template_name = 'mess_manager/update_mess_menu.html'

    def get(self, request, menu_id):
        if menu_id == 'new_day':
            # Provide an empty form for adding a new day
            form = MessMenuForm()
        else:
            # Fetch the menu item for updating an existing day
            menu_item = get_object_or_404(MessMenu, pk=menu_id)
            form = MessMenuForm(instance=menu_item)

        return render(request, self.template_name, {'form': form, 'menu_id': menu_id})

    def post(self, request, menu_id):
        if menu_id == 'new_day':
            # Handle form submission for adding a new day
            form = MessMenuForm(request.POST)
        else:
            # Handle form submission for updating an existing day
            menu_item = get_object_or_404(MessMenu, pk=menu_id)
            form = MessMenuForm(request.POST, instance=menu_item)

        if form.is_valid():
            form.save()  # Save the form
            return redirect('mess_menu')  # Redirect to the mess_menu view

        return render(request, self.template_name, {'form': form, 'menu_id': menu_id})

class StudentDetailView(View):
    def get(self, request, roll_number):
        student = Student.objects.get(roll_number=roll_number)
        return render(request, 'mess_manager/student_detail.html', {'student': student})

       

class BreakdownChartView(View):
    def get(self, request, roll_number):
        try:
            student = Student.objects.get(roll_number=roll_number)
            # Retrieve breakdown chart data for the student
            breakdown_data = {
                'roll_number': student.roll_number,
                'name': student.name,
                'paid_fees': student.paid_fees,
                'remaining_fees': student.remaining_fees,
                # Add other breakdown data as needed
            }

            return render(request, 'mess_manager/breakdown_chart.html', {'breakdown_data': breakdown_data})

        except Student.DoesNotExist:
            # Handle the case where the student with the given roll_number does not exist
            return render(request, 'mess_manager/student_not_found.html')


class AddWorkerStaffView(View):
    def get(self, request):
        if not request.user.is_authenticated or request.user.is_student:
            return HttpResponseForbidden("You don't have permission to perform this action.")
        form = AddWorkerStaffForm()
        return render(request, 'mess_manager/add_worker_staff.html', {'form': form})

    def post(self, request):
        if not request.user.is_authenticated or request.user.is_student:
            return HttpResponseForbidden("You don't have permission to perform this action.")
        form = AddWorkerStaffForm(request.POST)
        if form.is_valid():
            # Process the form data and save to the database
            # Example: username = form.cleaned_data['username']
            # Example: password = form.cleaned_data['password']
            # Add logic to save the data to the database

            return redirect('add_worker_staff_success')  # Redirect to success page or another view

        return render(request, 'mess_manager/add_worker_staff.html', {'form': form})




from django.shortcuts import get_object_or_404

from django.views.generic import View
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden
from mess_manager.models import MessMenu

from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .forms import MessMenuForm
from .models import MessMenu

from django.db.models import Case, When, Value, IntegerField
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponseForbidden
from .models import MessMenu

from django.http import HttpResponseRedirect

from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views import View
from .forms import MessMenuForm
from .models import MessMenu
from django.http import HttpResponseRedirect

class MessMenuView(View):
    template_name = 'mess_manager/mess_menu.html'

    def get(self, request):
        if not request.user.is_authenticated or request.user.is_student:
            return HttpResponseForbidden("You don't have permission to perform this action.")

        # Define the order of days
        day_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        # Fetch all distinct days
        days = MessMenu.objects.values_list('day', flat=True).distinct()

        # Create a conditional expression to map day names to integers for ordering
        order_conditions = [When(day=day, then=Value(index)) for index, day in enumerate(day_order)]

        # Order the days based on the predefined order
        ordered_days = days.annotate(
            order=Case(*order_conditions, default=Value(len(day_order)), output_field=IntegerField())
        ).order_by('order')

        # Create a dictionary to hold menu items for each day
        menu_items = {}
        for day in ordered_days:
            menu_items[day] = MessMenu.objects.filter(day=day)

        # Pass the form instance to the template
        form = MessMenuForm()
        
        return render(request, self.template_name, {'menu_items': menu_items, 'form': form})

    def post(self, request):
        if not request.user.is_authenticated or request.user.is_student:
            return HttpResponseForbidden("You don't have permission to perform this action.")

        form = MessMenuForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path_info)  # Redirect to the same page after successful submission
        else:
            # If the form is invalid, re-render the page with the form and error messages
            return render(request, self.template_name, {'form': form})



class ExtraMealMenuView(View):
    def get(self, request):
        extra_meals = ExtraMealMenu.objects.all()
        return render(request, 'mess_manager/extra_meal_menu.html', {'extra_meals': extra_meals})

    # Add logic for handling form submissions if needed    

        
class StudentListView(View):
    def get(self, request):
        students = Student.objects.exclude(rollno__in=[0, 1])
        return render(request, 'mess_manager/student-list.html', {'students': students})
    
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        logout(request)
        return redirect('home')


from django.db.models import Count

def view_bookings(request):
    if not request.user.is_authenticated or request.user.is_student:
            return HttpResponseForbidden("You don't have access to this page.")

    if request.method == "POST":
        date = request.POST.get('date')
        time = request.POST.get('time')

        # Calculate total number of students
        total_students = Student.objects.exclude(rollno__in=[0, 1]).count()

        # Calculate total number of cancellations for the specified date and time
        total_cancellations = BaseMealPrecancellation.objects.filter(date=date, time=time).count()

        extra_items_counts = BookingExtraItems.objects.filter(date=date, time=time).values('extra_item').annotate(count=Count('extra_item'))


        # Calculate remaining students
        remaining_students = total_students - total_cancellations

        # Pass data to the template
        context = {
            'total_students': total_students,
            'total_cancellations': total_cancellations,
            'remaining_students': remaining_students,
            'extra_items_counts': extra_items_counts,
        }
        return render(request, 'mess_manager/view_bookings.html', context)
    

    return render(request, 'mess_manager/view_bookings.html')
