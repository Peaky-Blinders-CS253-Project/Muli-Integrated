from django.urls import path
from .views import IndexView, StudentListView, MealListView, MessRecordListView, StudentDetailView, SecureView, UserLoginView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('meals/', MealListView.as_view(), name='meal_list'),
    path('mess_records/', MessRecordListView.as_view(), name='mess_record_list'),
    path('students/<int:student_id>/', StudentDetailView.as_view(), name='student_detail'),
    path('secure/', SecureView.as_view(), name='secure'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    # Add other paths as needed
]
