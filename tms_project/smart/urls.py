from django.urls import path
from . import views
from .views import admin_reports

urlpatterns = [

    # =========================
    # DASHBOARD
    # =========================


    # =========================
    # MANAGERS
    # =========================
    path('manage-managers/', views.manage_managers, name='manage_managers'),
    path('managers/add/', views.add_manager, name='add_manager'),
    path('managers/edit/<int:id>/', views.edit_manager, name='edit_manager'),
    path('managers/delete/<int:id>/', views.delete_manager, name='delete_manager'),

    # =========================
    # TRAINERS
    # =========================
    path('manage-trainers/', views.manage_trainers, name='manage_trainers'),
    path('trainers/add/', views.add_trainer, name='add_trainer'),

    path('manage-trainees/', views.manage_trainees, name='manage_trainees'),
    path('training-programs/', views.training_programs, name='training_programs'),
    path('managers/edit/<int:id>/', views.edit_manager, name='edit_manager'),
    path('trainers/edit/<int:id>/', views.edit_trainer, name='edit_trainer'),
    path('trainers/delete/<int:id>/', views.delete_trainer, name='delete_trainer'),

    path('trainees/add/', views.add_trainee, name='add_trainee'),
    path('trainees/edit/<int:id>/', views.edit_trainee, name='edit_trainee'),
    path('trainees/delete/<int:id>/', views.delete_trainee, name='delete_trainee'),

    path('programs/edit/<int:id>/', views.edit_program, name='edit_program'),
    path('programs/delete/<int:id>/', views.delete_program, name='delete_program'),
    path('programs/add/', views.add_program, name='add_program'),
    path('program/<int:id>/', views.program_detail, name='program_detail'),
    path('admin-reports/', admin_reports, name='admin_reports'),

    path('admin-notification/', views.admin_notifications, name='admin_notification'),
    path('admin-mark-read/<int:id>/', views.admin_mark_read, name='admin_mark_read'),
    path('admin-delete/<int:id>/', views.admin_delete_notification, name='admin_delete'),
    path('admin-mark-all/', views.admin_mark_all_read, name='admin_mark_all'),

]