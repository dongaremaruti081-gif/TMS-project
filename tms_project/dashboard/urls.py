from django.urls import path
from . import views

urlpatterns = [

    # 🔥 MAIN REDIRECT (LOGIN NANTAR HE USE KAR)
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),

    # ROLE BASED DASHBOARDS
    path('superadmin/', views.superadmin_dashboard, name='superadmin_dashboard'),
    path('adminapp/', views.admin_dashboard, name='admin_dashboard'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('trainer/', views.trainer_dashboard, name='trainer_dashboard'),
    path('trainee/', views.trainee_dashboard, name='trainee_dashboard'),

    # OTHER
    path('activity-logs/', views.activity_logs, name='activity_logs'),
    path('base_dashboard/', views.dashboard_base, name='base_dashboard'),
    path('all-users/', views.all_users, name='all_users'),
    path('users/<str:role>/', views.users_by_role, name='users_by_role'),
# urls.py
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
# urls.py
    path('courses/', views.all_courses, name='all_courses'),
]