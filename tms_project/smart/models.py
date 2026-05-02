from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# 📚 Training Program Model
class TrainingProgram(models.Model):
    CATEGORY_CHOICES = [
        ('Leadership', 'Leadership'),
        ('Technical', 'Technical'),
        ('Sales', 'Sales'),
        ('Compliance', 'Compliance'),
        ('Management', 'Management'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Upcoming', 'Upcoming'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    duration = models.CharField(max_length=100)
    start_date = models.DateField()

    capacity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # ✅ Auto count enrolled students
    def enrolled_count(self):
        return self.enrollments.count()

    # ✅ Calculate percentage
    def progress_percent(self):
        if self.capacity > 0:
            return int((self.enrolled_count() / self.capacity) * 100)
        return 0

class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
    ]

    trainee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'Trainee'}
    )

    training = models.ForeignKey(
        TrainingProgram,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    progress = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    enrolled_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # 🔥 AUTO CREATE / UPDATE Progress
        from trainer.models import Progress

        Progress.objects.update_or_create(
            trainee=self.trainee,
            training=self.training,
            defaults={
                "percentage": self.progress
            }
        )

    def __str__(self):
        return f"{self.trainee} - {self.training}"




# 👨‍🏫 Trainer Assignment (Optional but powerful)
class TrainerAssignment(models.Model):
    trainer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'Trainer'}
    )

    training = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE)

    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trainer} -> {self.training}"





from django.db import models
from django.conf import settings
class AdminNotification(models.Model):

    ROLE_CHOICES = (
        ('SuperAdmin', 'SuperAdmin'),
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Trainer', 'Trainer'),
        ('Trainee', 'Trainee'),
    )

    title = models.CharField(max_length=255)
    message = models.TextField()

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        null=True,
        blank=True
    )

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title