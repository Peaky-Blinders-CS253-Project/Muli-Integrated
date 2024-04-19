# students/views.py
from django.shortcuts import render, redirect
from django.views import View
from .models import Student, BaseMealPrecancellation, BookingExtraItems
from .forms import StudentCardForm
from .forms import StudentLoginForm
from django.contrib.auth import authenticate, login, logout
from .forms import StudentRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .models import ExtraItem, BreakdownChartExtra, BreakdownChart
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.views.generic import ListView, DetailView
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.generic import FormView
from .forms import StudentLoginForm
from django.urls import reverse_lazy
import datetime

class ExtraItemListView(ListView):
    model = ExtraItem
    template_name = 'students/extra_item_list.html'
    context_object_name = 'extra_items'

class ExtraItemDetailView(DetailView):
    model = ExtraItem
    template_name = 'extra_item_detail.html'
    context_object_name = 'extra_item'

from django.http import HttpResponseBadRequest

def book_extra_item(request, rollno):
    if not request.user.is_authenticated or request.user.rollno != rollno:
        return HttpResponseForbidden("You are not authorized to access this page.")

    if request.method == 'POST':
        # Get data from the form
        extra_date = request.session.get('extraDate')
        extra_time = request.session.get('extraTime')
        extra_item_id = request.POST.get('extra_item')  # Assuming the value is the ID of the extra item

        # Save the data to the BookingExtraItems model
        booking_extra_item = BookingExtraItems.objects.create(
            rollno=rollno,
            date=extra_date,
            time=extra_time,
            extra_item=extra_item_id
            # Add other fields if needed
        )
    
        # Redirect the user to a success page
        return redirect('meal_cancel', rollno=rollno)  # Replace 'meal_cancel' with the URL name of your success page

    # Handle GET requests or invalid form submissions
    return render(request, 'book_extra_item.html')

from .models import BookingExtraItems

from django.db.models import Value, F, CharField

def booking_extra_items_chart(request):
    if request.user.is_authenticated:
        rollno = request.user.rollno
        booking_extra_items = BookingExtraItems.objects.filter(rollno=rollno)
        
        # Fetch prices for all extra items
        extra_item_prices = ExtraItem.objects.all()
        
        # Pass booking_extra_items and extra_item_prices to the template
        return render(request, 'booking_extra_item_chart.html', {
            'booking_extra_items': booking_extra_items,
            'extra_item_prices': extra_item_prices
        })
    else:
        return HttpResponseForbidden("You are not authorized to access this page.")

def book_extra_item(request, pk):
    extra_item = ExtraItem.objects.get(pk=pk)
    student = Student.objects.get(username=request.user.username)  # Assuming you have a OneToOneField linking Student to User
    quantity = int(request.POST['quantity'])
    price = extra_item.price * quantity

    # Set the default base meal price (replace this with your actual logic)
    base_meal_price = 0.00  # Example base meal price

    # Create or update the breakdown chart for the student
    breakdown_chart, _ = BreakdownChart.objects.get_or_create(student=student, date=date.today())
    breakdown_chart.base_meal_price = base_meal_price  # Set the base meal price
    breakdown_chart.save()

    # Create or update the breakdown chart extra for the student
    breakdown_chart_extra, _ = BreakdownChartExtra.objects.get_or_create(breakdown_chart=breakdown_chart, extra_item=extra_item,user_name=student)
    breakdown_chart_extra.quantity += quantity
    breakdown_chart_extra.price += price
    breakdown_chart_extra.save()

    # Update the total extras price and total cost in the breakdown chart
    breakdown_chart.total_extras_price += price
    breakdown_chart.total_cost += price
    breakdown_chart.save()

    return redirect('booking_success')

def booking_success(request):
    return render(request, 'students/extrabook_success.html')



def student_breakdown_view(request):
    student = request.user  # Assuming you have a OneToOneField linking Student to User
    breakdowns = BreakdownChart.objects.filter(student=student)
    breakdown_extras = BreakdownChartExtra.objects.filter(breakdown_chart__student=student)

    return render(request, 'students/student_breakdown.html', {'breakdowns': breakdowns, 'breakdown_extras': breakdown_extras})





class StudentdashboardView(View):
    
    def get(self, request, rollno, *args, **kwargs):
        if request.user.is_student and request.user.rollno == rollno:
            return render(request, 'students/student_dashboard.html', {'rollno': rollno})
        else:
            return HttpResponseForbidden("You are not authorized to access this page.")
        
        # Check if the roll number in the URL matches the logged-in user's roll number
        #if str(request.user.rollno) != rollno:
        #   return HttpResponseForbidden("")
        
        # Your view logic here
        #if not request.user.is_student and request.user.rollno != rollno and request.user.rollno == 0 :
        #    return HttpResponseForbidden("You are not authorized to access this page.")



from django.contrib.auth.hashers import check_password

class StudentchangepasswordView(FormView):
    template_name = 'students/student_register.html'
    form_class = StudentRegistrationForm

    def form_valid(self, form):
        # Extract form data
        rollno = form.cleaned_data['rollno']
        password = form.cleaned_data['password']
        newpassword = form.cleaned_data['newpassword']
        
        try:
            # Get the student instance from the database
            student = Student.objects.get(rollno=rollno)
            # Check if the provided password matches the hashed password in the database
            if check_password(password, student.password):
                # Update the password for the existing user
                student.password = make_password(newpassword)
                # Save the updated student object
                student.save()
                
                # Redirect to student_dashboard with rollno as keyword argument
                # Redirect to the dashboard after successful password change
                return redirect('student_login')
            else:
                # Password does not match, return form with error message
                form.add_error('password', 'Incorrect password')
                return self.form_invalid(form)

        except Student.DoesNotExist:
            # Student not found, return form with error message
            form.add_error('rollno', 'Student not found')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('student_dashboard')

   
from django.contrib import messages

class StudentLoginView(FormView):
    template_name = 'students/student_login.html'
    form_class = StudentLoginForm

    def form_valid(self, form):
        roll_no = form.cleaned_data['roll_no']
        password = form.cleaned_data['password']

        # Authenticate only if the user is a student
        user = authenticate(rollno=roll_no, password=password)
        if user is not None:
            if user.is_student:
                login(self.request, user)
                success_url = reverse_lazy('student_dashboard', kwargs={'rollno': user.rollno})
                return redirect(success_url)
            else:
                messages.error(self.request, 'You are not authorized to access this page.')
        else:
            messages.error(self.request, 'Invalid username or password')
        return self.form_invalid(form)

from mess_manager.forms import MessMenuForm
from mess_manager.models import MessMenu


from django.views.generic import View
from django.shortcuts import render
from django.db.models import Case, Value, When, IntegerField
class StudentMessMenuView(View):
    template_name = 'students/mess_menu.html'

    def get(self, request):
        if not request.user.is_authenticated or not request.user.is_student:
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
        
        return render(request, self.template_name, {'menu_items': menu_items})





class StudentLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')  # Redirect to student login page
        
import datetime
from django.http import JsonResponse

def base_meal_precancellations(request,rollno):
    return render(request, 'students/base_meal_precancellation.html')

from datetime import datetime
import datetime

def meal_cancel(request, rollno):
    if not request.user.is_student and request.user.rollno != rollno and request.user.rollno == 0:
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    if request.user.is_student and request.user.rollno == rollno:
        context = {'rollno': rollno}
        
        if request.method == 'POST':
            cancel_date = request.POST.get('canceldate')
            cancel_time = request.POST.get('canceltime')
            
            if datetime.today().date() >= datetime.strptime(cancel_date, '%Y-%m-%d').date():
                message = 'Please select a date greater than today.'
                context['message'] = message
                return render(request, 'students/meal_cancel.html', context)
            
            BaseMealPrecancellation.objects.create(rollno=request.user.rollno, date=cancel_date, time=cancel_time)
            message = 'Meal cancellation is successful.'
            context['message'] = message
            return render(request, 'students/meal_cancel.html', context)
        
        return render(request, 'students/meal_cancel.html', context)
    else:
        return HttpResponseForbidden("You are not authorized to access this page.")


from datetime import datetime


from django.utils import timezone

def extra_booking(request, rollno):
    if request.method == 'POST':
        extra_date = request.POST.get('extraDate')
        extra_time = request.POST.get('extraTime')
        
        # Check if the selected date is a future date
        selected_date = datetime.strptime(extra_date, '%Y-%m-%d').date()
        if selected_date <= timezone.now().date():
            # Return an error message or handle the case where the selected date is in the past
            message = "Selected date must be a future date."
            return render(request, 'students/meal_cancel.html',{'message':message})
        
        # Get the day of the week for the selected date
        day_of_week = selected_date.strftime('%A')
        
        # Fetch weekly items for the selected day of the week
        weekly_items = ExtraItem.objects.filter(Day=day_of_week, Type='Weekly')
        
        # Fetch special items for the selected date and time
        special_items = ExtraItem.objects.filter(Date=extra_date, Type='Special')
        
        # Fetch regular items for the selected date and time
        regular_items = ExtraItem.objects.filter(Date=extra_date, Time=extra_time, Type='Regular')
        
        # Render the template with the retrieved items
        return render(request, 'students/meal_cancel.html', {'weekly_items': weekly_items,
                                                             'special_items': special_items,
                                                             'regular_items': regular_items})
    else:
        # Handle GET request (initial load of the page)
        return render(request, 'students/meal_cancel.html')

from datetime import datetime

def show_extra(request,rollno):
    if not request.user.is_student and request.user.rollno != rollno and request.user.rollno == 0:
            return HttpResponseForbidden("You are not authorized to access this page.")
    if request.method == 'POST':
        extra_date = request.POST.get('extraDate')
        extra_time = request.POST.get('extraTime')

        if datetime.today().date() >= datetime.strptime(extra_date, '%Y-%m-%d').date():
                messagebook = 'Please select a date greater than today.'
                return render(request, 'students/meal_cancel.html',{'rollno':rollno,'messagebook':messagebook})
        
        # Get the day of the week for the selected date
        day_of_week = datetime.strptime(extra_date, '%Y-%m-%d').strftime('%A').lower()
        
        # Fetch weekly items for the selected day of the week
        weekly_items = ExtraItem.objects.filter(Day=day_of_week, Type='weekly')
        
        # Fetch special items for the selected date and time
        special_items = ExtraItem.objects.filter(Date=extra_date,Time=extra_time , Type='special')
        
        # Fetch regular items for the selected date and time
        regular_items = ExtraItem.objects.filter(Type='regular')

        request.session['extraDate'] = extra_date
        request.session['extraTime'] = extra_time
        
        # Render the template with the retrieved items
        return render(request, 'students/show_extra.html', {'rollno': rollno,'weekly_items': weekly_items,
                                                             'special_items': special_items,
                                                             'regular_items': regular_items})
    else:
        # Handle GET request (initial load of the page)
        return render(request, 'students/meal_cancel.html')

def book_extra_item(request, rollno):
    if not request.user.is_student and request.user.rollno != rollno and request.user.rollno == 0 :
            return HttpResponseForbidden("You are not authorized to access this page.")
    if request.method == 'POST':
        # Get data from the form
        extra_date = request.session.get('extraDate')
        extra_time = request.session.get('extraTime')
        extra_item_id = request.POST.get('extra_item')  # Assuming the value is the ID of the extra item

        # Save the data to the BookingExtraItems model
        booking_extra_item = BookingExtraItems(
            rollno=rollno,
            date=extra_date,
            time=extra_time,
            extra_item=extra_item_id
            # Add other fields if needed
        )
        booking_extra_item.save()


        # Optionally, you can redirect the user to a success page
        return redirect('meal_cancel',rollno=rollno)  # Replace 'success_page' with the URL name of your success page

    # Handle GET requests or invalid form submissions


def get_extra_items(request):
    date = request.GET.get('date')
    time = request.GET.get('time')

    # Retrieve extra items based on date and time
    extra_items = ExtraItem.objects.filter(Date=date, Time=time).values('id', 'name', 'price')

    # Return extra items as JSON response
    return JsonResponse(list(extra_items), safe=False)


def cancel_meal(request, rollno):
    if request.method == 'POST':
        cancel_date = request.POST.get('canceldate')
        cancel_time = request.POST.get('canceltime')
        if datetime.date.today() >= datetime.datetime.strptime(cancel_date, '%Y-%m-%d').date():
            message = 'Please select a date greater than today.'
            return redirect('base_meal_precancellation')
        BaseMealPrecancellation.objects.create(rollno=request.user.rollno, date=cancel_date, time=cancel_time)
        message = 'Meal cancellation is successful.'
        return redirect('base_meal_precancellation')
    return redirect('base_meal_precancellation')

class StudentCardView(View):
    def get(self, request, roll_number):
        student = Student.objects.get(roll_number=roll_number)
        form = StudentCardForm()  # You might want to initialize the form with initial data if needed
        return render(request, 'students/student_card.html', {'student': student, 'form': form})









 