from django.db import models
from django.conf import settings
from smart.models import TrainingProgram


class Certificate(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    training = models.ForeignKey(
        TrainingProgram,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    issued_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.training}"


from django.db import models
from django.conf import settings
   # existing course

User = settings.AUTH_USER_MODEL

class Module(models.Model):
    course = models.ForeignKey('smart.TrainingProgram', on_delete=models.CASCADE,related_name='modules')
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    LESSON_TYPE = (
        ('video', 'Video'),
        ('doc', 'Document'),
        ('quiz', 'Quiz'),
    )

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)
    lesson_type = models.CharField(max_length=10, choices=LESSON_TYPE)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'lesson')




from django.db import models
from django.conf import settings
class Assignment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ]

    title = models.CharField(max_length=200)
    course = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    grade = models.CharField(max_length=10, blank=True, null=True)

    from django.utils import timezone

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return self.title


from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class SkillProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100)
    percentage = models.IntegerField()

    def __str__(self):
        return f"{self.skill_name} - {self.percentage}%"


class StudyHour(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    hours = models.IntegerField()

    def __str__(self):
        return f"{self.month} - {self.hours}h"

