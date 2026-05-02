# trainee/urls.py

from django.urls import path
from .views import my_courses

from . import views   # ✅ ADD THIS LINE

urlpatterns = [
    path('my-courses/', my_courses, name='my_courses'),
    path('course/<int:course_id>/', views.course_content, name='course_content'),
    path('lesson-complete/<int:lesson_id>/', views.mark_complete, name='mark_complete'),
    path('assignments/', views.assignments, name='assignments'),
    path('progress/', views.my_progress, name='my_progress'),
    path('certificates/', views.my_certificates, name='my_certificates'),

    path('assignment/start/<int:id>/', views.start_assignment, name='start_assignment'),
    path('assignment/view/<int:id>/', views.view_assignment, name='view_assignment'),
    path('materials/', views.materials, name='materials'),

]