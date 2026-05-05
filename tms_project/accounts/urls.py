
from .views import home, login_view, register_view
from . import views
from .views import profile_view, change_password
from django.urls import path
from .views import notifications_view, mark_all_read, delete_notification
from django.contrib.auth import views as auth_views
from .views import logout_view
from django.urls import path
from . import views
from .views import logout_view
from .views import reports_analytics



urlpatterns = [
    # Static Pages
    path('about/', views.about, name='about'),
    path('features/', views.features, name='features'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),

    # Auth Pages
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),

    path('', home, name='home'),              # 🏠 Home
    path('login/', login_view, name='login'), # 🔐 Login
    path('register/', register_view, name='register'), # 📝 Register
    path('manage-admins/', views.manage_admins, name='manage_admins'),
    path('add-adminapp/', views.add_admin, name='add_admin'),
    path('profile/', profile_view, name='profile'),
    path('change-password/', change_password, name='change_password'),


    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/read/<int:id>/', views.mark_as_read, name='mark_as_read'),
    path('notifications/read-all/', views.mark_all_read, name='mark_all_read'),
    path('notifications/delete/<int:id>/', views.delete_notification, name='delete_notification'),

    path('edit-adminapp/<int:id>/', views.edit_admin, name='edit_admin'),
    path('delete-adminapp/<int:id>/', views.delete_admin, name='delete_admin'),
    path('toggle-adminapp/<int:id>/', views.toggle_admin_status, name='toggle_admin_status'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),

    path('logout/', logout_view, name='logout'),
    path('get-courses/<int:emp_id>/', views.get_courses, name='get_courses'),








    path('assign-training/', views.assign_training, name='assign_training'),



    # =====================================
    # EMPLOYEE MANAGEMENT
    # =====================================
    path('employees/', views.employee_management, name='employee_management'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('delete-employee/<int:id>/', views.delete_employee, name='delete_employee'),

    # =====================================
    # ATTENDANCE
    # =====================================
    path('attendance/', views.attendance_view, name='attendance'),

    # =====================================
    # PERFORMANCE REPORT
    # =====================================

    path('reports-analytics/', reports_analytics, name='reports_analytics'),

    # =====================================
    # PROFILE
    # =====================================
    path('profile/', views.profile_view, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),

    # =====================================
    # NOTIFICATIONS
    # =====================================




    path('noti/',views.noti_view,name='noti'),

]


