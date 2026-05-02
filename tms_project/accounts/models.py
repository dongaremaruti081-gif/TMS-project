from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser

from django.conf import settings
from django.contrib.auth import get_user_model



class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('SuperAdmin', 'SuperAdmin'),
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Trainer', 'Trainer'),
        ('Trainee', 'Trainee'),
    )

    # 🔥 Role field
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


    department = models.CharField(max_length=100, null=True, blank=True)
    # 🔥 Additional fields
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    # ✅ NEW FIELD (PROFILE IMAGE)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username

from django.db import models
from django.conf import settings

class Notification(models.Model):

    ROLE_CHOICES = (
        ('SuperAdmin', 'SuperAdmin'),
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Trainer', 'Trainer'),
        ('Trainee', 'Trainee'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)

    title = models.CharField(max_length=255)
    message = models.TextField()

    notification_type = models.CharField(max_length=20, default='info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)




class Attendance(models.Model):

    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Leave', 'Leave'),
    ]

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    training = models.ForeignKey(   # ✅ ADD THIS
        "smart.TrainingProgram",
        on_delete=models.CASCADE
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Present'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} - {self.training.title} - {self.date}"

# =====================================================
# TRAINING MODEL (✔️ FIXED - MAIN PART)
# =====================================================
class TrainingManager(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    trainer_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    #description = models.TextField(
      #  null=True,
       # blank=True
    #)

  #  progress = models.IntegerField(default=0)

    #status = models.CharField(
       # max_length=20,
       # choices=STATUS_CHOICES,
       # default='pending'
   # )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.employee.username}"


# =====================================================
# Notification Model
# =====================================================
User = get_user_model()
from django.db import models
from django.conf import settings
class Noti(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, default='info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Report Model
# =====================================================
class Report(models.Model):

    name = models.CharField(max_length=200)
    generated_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# =====================================================
# Team Skills Assessment Model
# =====================================================
class TeamSkillAssessment(models.Model):

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    technical = models.IntegerField(default=0)
    communication = models.IntegerField(default=0)
    leadership = models.IntegerField(default=0)
    problem_solving = models.IntegerField(default=0)
    teamwork = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.employee.username
