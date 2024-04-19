# mess_manager/urls.py

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import MessMenuView, ExtraMealMenuView, \
    StudentDetailView, BreakdownChartView, AddWorkerStaffView, BaseMealChargeView, AddStudentSuccessView, UpdateMessMenuView
from .views import ManagerDashboardView, ManagerLoginView, StudentListView
from .views import ExtraItemList, ExtraItemCreate, ExtraItemUpdate, ExtraItemDelete, BaseMealChargeSuccessView   
from .views import logout_view
from .views import AddStudentView,ExtraItemCreate,delete_extra_item,update_price
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='mess_manager/manager_login.html'), name='login'),
    #path('logout/', LogoutView.as_view(next_page='home'), name='log-out'),
    path('logout/', logout_view, name='logout'),
    path('manager-login/', ManagerLoginView.as_view(), name='manager_login'),
    path('manager-dashboard/', ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('delete-menu-item/<int:pk>/', MessMenuView.as_view(), name='delete_menu_item'),
    path('mess-menu/', MessMenuView.as_view(), name='mess_menu'),
    path('update_mess_menu/<int:menu_id>/', UpdateMessMenuView.as_view(), name='update_mess_menu'),
    path('extra-meal-menu/', ExtraMealMenuView.as_view(), name='extra_meal_menu'),
    path('add-student/', AddStudentView ,name ='AddStudentView'),
    path('add-student/success/', AddStudentSuccessView.as_view(), name='add_student_success'),
    path('student-detail/<str:roll_number>/', StudentDetailView.as_view(), name='student_detail'),
    path('breakdown-chart/<str:roll_number>/', BreakdownChartView.as_view(), name='breakdown_chart'),
    path('add-worker-staff/', AddWorkerStaffView.as_view(), name='add_worker_staff'),
    path('set-base-meal-charge/', BaseMealChargeView.as_view(), name='set_base_meal_charge'),
    path('base-meal-charge-success/', BaseMealChargeSuccessView.as_view(), name='base_meal_charge_success'),
    # Add other URLs for mess manager views
    path('student-list/', StudentListView.as_view(), name='student_list'),

    path('extraitem/',ExtraItemCreate, name='extraitemcreate'),
   # path('extraitem/create/', ExtraItemCreate.as_view(), name='extraitem_create'),
    #path('extraitem/<int:pk>/update/', ExtraItemUpdate.as_view(), name='extraitem_update'),
    #path('extraitem/<int:pk>/delete/', ExtraItemDelete.as_view(), name='extraitem_delete'),
    path('delete/<int:item_id>/', delete_extra_item, name='delete_extra_item'),
    path('update-price/<int:extra_id>/', update_price, name='update_price'),
    path('view-bookings/',views.view_bookings,name='view_bookings'),

]
