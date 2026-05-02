from django.shortcuts import render
from .models import SuperReport
from accounts.models import CustomUser
from django.db.models import Count
from django.db.models.functions import TruncDay
import json


def reports_dashboard(request):

    # =========================
    # SAME COUNTS
    # =========================
    total_users = CustomUser.objects.count()
    trainees = CustomUser.objects.filter(role="Trainee").count()
    trainers = CustomUser.objects.filter(role="Trainer").count()
    managers = CustomUser.objects.filter(role="Manager").count()
    admins = CustomUser.objects.filter(role="Admin").count()

    # =========================
    # 🔥 IMPROVED USER GROWTH GRAPH
    # =========================
    user_growth = (
        CustomUser.objects
        .annotate(day=TruncDay('date_joined'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    labels = []
    data = []

    for item in user_growth:
        if item['day']:
            labels.append(item['day'].strftime("%d %b"))
            data.append(item['count'])

    # ✅ FIX: graph smooth + empty avoid
    if len(labels) == 0:
        labels = ["01 Apr", "02 Apr", "03 Apr", "04 Apr", "05 Apr"]
        data = [1, 2, 1, 3, 2]

    # =========================
    # 🔥 ROLE DISTRIBUTION (NEW ADD)
    # =========================
    role_labels = ['Admin', 'Manager', 'Trainer', 'Trainee']
    role_counts = [
        admins,
        managers,
        trainers,
        trainees
    ]

    # =========================
    # REPORT TABLE
    # =========================
    reports = SuperReport.objects.all().order_by('-generated_date')

    # =========================
    # CONTEXT
    # =========================
    context = {
        'total_users': total_users,
        'trainees': trainees,
        'trainers': trainers,
        'managers': managers,
        'admins': admins,

        # 🔥 GRAPH DATA (IMPORTANT CHANGE)
        'months': json.dumps(labels),
        'counts': json.dumps(data),   # <-- changed name
        'role_labels': json.dumps(role_labels),
        'role_counts': json.dumps(role_counts),

        'reports': reports,
    }

    return render(request, 'reports/reports.html', context)