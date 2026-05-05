import os
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_migrate)
def create_superadmin(sender, **kwargs):
    username = os.getenv("SUPERADMIN_USERNAME")
    email = os.getenv("SUPERADMIN_EMAIL")
    password = os.getenv("SUPERADMIN_PASSWORD")

    # safety check
    if not username or not password:
        return

    if not CustomUser.objects.filter(username=username).exists():
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.role = 'SuperAdmin'
        user.is_superuser = True
        user.is_staff = True
        user.save()

        print("✅ SuperAdmin created successfully")
    else:
        print("⚡ SuperAdmin already exists")