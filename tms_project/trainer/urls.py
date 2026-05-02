from django.urls import path
from . import views

urlpatterns = [
    path('my_trainings/', views.my_trainings, name='my_trainings'),
    path("my_progress/", views.progress_view, name="trainer_progress"),
    path('create_content/', views.create_content, name='create_content'),
    path('content_list/', views.content_list, name='content_list'),
    path('upload-material/', views.upload_material, name='upload_material'),
    path('materials/', views.material_list, name='material_list'),
    path('add_material/', views.add_material, name='add_material'),
    path('edit_material/<int:id>/', views.edit_material, name='edit_material'),
    path('delete_material/<int:id>/', views.delete_material, name='delete_material'),

    path('course_list/', views.course_list, name='course_list'),
    path('delete/<int:id>/', views.delete_course, name='delete_course'),
    path('create_content/', views.create_content, name='create_content'),
    path('content_list/', views.content_list, name='content_list'),
    path('create_course/', views.create_course, name='create_course'),
    path('add_trainings',views.add_training,name='add_trainings'),

    path('create-assignment/', views.create_assignment, name='create_assignment'),
    path('assignment-list/', views.assignment_list, name='assignment_list'),

]