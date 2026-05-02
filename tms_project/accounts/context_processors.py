from accounts.models import Notification, Noti
from smart.models import AdminNotification

def base_context(request):

    notification_count = 0

    if request.user.is_authenticated:
        user = request.user

        # ONLY USER SPECIFIC NOTIFICATIONS
        notif_count = Notification.objects.filter(
            user=user,
            is_read=False
        ).count()

        noti_count = Noti.objects.filter(
            user=user,
            is_read=False
        ).count()

        notification_count = notif_count + noti_count

    return {
        'notification_count': notification_count
    }


def global_settings(request):
    return {
        "site_name": "TMS System",
    }
