from django.db import models

class SuperReport(models.Model):
    STATUS_CHOICES = (
        ('Completed', 'Completed'),
        ('Processing', 'Processing'),
    )

    name = models.CharField(max_length=200)
    generated_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name