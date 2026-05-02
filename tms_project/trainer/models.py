
from django.db import models
from django.conf import settings
from smart.models import TrainingProgram


class Progress(models.Model):
    trainee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='training_progress',
        null=True,
        blank=True
    )

    training = models.ForeignKey(
        TrainingProgram,
        on_delete=models.CASCADE,
        related_name='trainee_progress'
    )

    percentage = models.PositiveIntegerField(default=0)
    completed_assignments = models.PositiveIntegerField(default=0)
    total_assignments = models.PositiveIntegerField(default=10)
    quiz_score = models.PositiveIntegerField(default=0)
    attendance_percentage = models.PositiveIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trainee.username} - {self.training.title}"

    @property
    def performance_status(self):
        if self.percentage >= 90:
            return "Excellent"
        elif self.percentage >= 70:
            return "Good"
        return "Needs Improvement"





# 📚 Training (keep if needed for dashboard stats)



#

from django.db import models

class Content(models.Model):

    CONTENT_TYPES = [
        ('document', 'Document'),
        ('video', 'Video'),
        ('image', 'Image'),

    ]

    CATEGORY_CHOICES = [
        ('Lecture Notes', 'Lecture Notes'),
        ('Assignment', 'Assignment'),
        ('Project', 'Project'),
    ]

    DIFFICULTY_LEVEL = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    # 🔥 FIXED: Using TrainingProgram (as you decided)
    course = models.ForeignKey(
        'smart.TrainingProgram',
        on_delete=models.CASCADE,
        related_name='contents'
    )

    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPES
    )

    title = models.CharField(max_length=200)

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField(blank=True, null=True)


    duration = models.IntegerField(default=0)

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_LEVEL,
        default='beginner'
    )

    file = models.FileField(
        upload_to='content/',
        blank=True,
        null=True
    )



    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# 📄 Material
class Material(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    training = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE,null=True,blank=True)  # ✅ ADD THIS

    def __str__(self):
        return self.title




# ⭐ Feedback
class Feedback(models.Model):
    trainer = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )

    def __str__(self):
        return f"{self.trainer} - {self.rating}"



class Session(models.Model):
    course = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE)
    trainer = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course.title} - {self.date}"


from django.db import models

# Create your models here.
class Question(models.Model):
    assignment = models.ForeignKey('trainee.Assignment', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

