from django.urls import path
from . import views

urlpatterns = [
    path('', views.training_list, name='training_list'),
    path('add/', views.add_training, name='add_training'),
    path('courses/', views.courses, name='courses'),
]