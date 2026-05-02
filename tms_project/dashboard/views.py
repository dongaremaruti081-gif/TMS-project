from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import CustomUser
from.models import ActivityLog
from django.db.models import Q


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from accounts.models import Attendance

from django.db.models import Q
from django.utils import timezone   # (for previous error)

from trainer.models import Session
from datetime import timedelta

import json

from django.db.models.functions import TruncMonth
from django.db.models import Count


import json

from django.db.models.functions import TruncMonth
from django.db.models import Count



from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
import json

from accounts.models import Attendance

from accounts.models import TrainingManager
from smart.models import TrainingProgram

User = get_user_model()


# ===============================
# ROLE CHECKS
# ===============================
def is_superadmin(user):
    return user.is_authenticated and user.role == 'SuperAdmin'

def is_admin(user):
    return user.is_authenticated and user.role == 'Admin'

def is_manager(user):
    return user.is_authenticated and user.role == 'Manager'

def is_trainer(user):
    return user.is_authenticated and user.role == 'Trainer'

def is_trainee(user):
    return user.is_authenticated and user.role == 'Trainee'


# ===============================
# 🔥 AUTO REDIRECT AFTER LOGIN
# ===============================
@login_required
def dashboard_redirect(request):
    role = request.user.role

    if role == "SuperAdmin":
        return redirect('superadmin_dashboard')
    elif role == "Admin":
        return redirect('admin_dashboard')
    elif role == "Manager":
        return redirect('manager_dashboard')
    elif role == "Trainer":
        return redirect('trainer_dashboard')
    elif role == "Trainee":
        return redirect('trainee_dashboard')

    return redirect('login')

from django.db.models.functions import TruncDay
from django.db.models import Count
import json
from django.db.models.functions import TruncDay
from django.db.models import Count
from .models import Alert   # 👈 import alert
import json

@login_required
@user_passes_test(is_superadmin)
def superadmin_dashboard(request):

    search_query = request.GET.get('search', '')

    users = CustomUser.objects.all()

    # 🔍 SEARCH
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(full_name__icontains=search_query) |
            Q(role__icontains=search_query)
        )

    # 📊 BASIC COUNTS
    total_users = CustomUser.objects.count()
    trainees = CustomUser.objects.filter(role="Trainee").count()
    trainers = CustomUser.objects.filter(role="Trainer").count()
    managers = CustomUser.objects.filter(role="Manager").count()
    admins = CustomUser.objects.filter(role="Admin").count()
    active_sessions = CustomUser.objects.filter(is_active=True).count()

    # 🔥 DAILY USER GROWTH (FIXED & CLEAN)
    user_growth = CustomUser.objects.annotate(
        day=TruncDay('date_joined')
    ).values('day').annotate(
        count=Count('id')
    ).order_by('day')

    labels = []
    growth_data = []

    for item in user_growth:
        if item['day']:
            labels.append(item['day'].strftime("%d %b"))   # 15 Apr
            growth_data.append(item['count'])

    # ⚠️ IF NO DATA
    if not labels:
        labels = ["No Data"]
        growth_data = [0]

    # 🚨 REAL ALERT SYSTEM
    critical_alerts = Alert.objects.filter(
        alert_type="Critical",
        is_read=False
    ).count()

    recent_alerts = Alert.objects.order_by('-created_at')[:5]

    context = {
        'total_users': total_users,
        'trainees': trainees,
        'trainers': trainers,
        'managers': managers,
        'admins': admins,
        'active_sessions': active_sessions,

        # 🔥 REAL ALERT DATA
        'critical_alerts': critical_alerts,
        'recent_alerts': recent_alerts,

        'recent_logs': ActivityLog.objects.all().order_by('-timestamp')[:5],

        # 📊 CHART DATA
        'months': json.dumps(labels),
        'growth_data': json.dumps(growth_data),

        'search_query': search_query,
        'users': users,
        'user_distribution': json.dumps([
            trainees,
            trainers,
            managers,
            admins
        ])
    }

    return render(request, 'dashboard/superadmin_dashboard.html', context)
# ===============================
# ADMIN DASHBOARD
# ===============================
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import CustomUser, Notification
from dashboard.models import ActivityLog, Alert
from reports.models import SuperReport


# ROLE CHECK
def is_admin(user):
    return user.is_authenticated and user.role == 'Admin'

from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncWeek, TruncMonth
from django.shortcuts import render
import json
from smart.models import TrainingProgram
from django.db.models import Count

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):

    now = timezone.now()

    # =========================
    # 👥 USERS
    # =========================
    total_trainees = CustomUser.objects.filter(role='Trainee').count()
    total_trainers = CustomUser.objects.filter(role='Trainer').count()
    total_managers = CustomUser.objects.filter(role='Manager').count()

    # =========================
    # 📊 PROGRAMS
    # =========================
    active_programs = SuperReport.objects.filter(status='Processing').count()

    # ✅ FIXED (MONTH + YEAR)
    new_programs = SuperReport.objects.filter(
        generated_date__month=now.month,
        generated_date__year=now.year
    ).count()

    completed_programs = SuperReport.objects.filter(status='Completed').count()
    total_programs = SuperReport.objects.count()

    completion_rate = 0
    if total_programs > 0:
        completion_rate = round((completed_programs / total_programs) * 100)

    # =========================
    # 📈 GROWTH (TRAINEES)
    # =========================
    last_month = now.month - 1 if now.month > 1 else 12
    last_month_year = now.year if now.month > 1 else now.year - 1

    trainees_this_month = CustomUser.objects.filter(
        role='Trainee',
        date_joined__month=now.month,
        date_joined__year=now.year
    ).count()

    trainees_last_month = CustomUser.objects.filter(
        role='Trainee',
        date_joined__month=last_month,
        date_joined__year=last_month_year
    ).count()

    trainee_growth = 0
    if trainees_last_month > 0:
        trainee_growth = round(
            ((trainees_this_month - trainees_last_month) / trainees_last_month) * 100
        )

    # =========================
    # 👨‍🏫 TRAINER GROWTH
    # =========================
    trainers_this_month = CustomUser.objects.filter(
        role='Trainer',
        date_joined__month=now.month,
        date_joined__year=now.year
    ).count()

    trainers_last_month = CustomUser.objects.filter(
        role='Trainer',
        date_joined__month=last_month,
        date_joined__year=last_month_year
    ).count()

    new_trainers = trainers_this_month

    trainer_growth = 0
    if trainers_last_month > 0:
        trainer_growth = round(
            ((trainers_this_month - trainers_last_month) / trainers_last_month) * 100
        )

    # =========================
    # 📅 WEEKLY DATA (DYNAMIC)
    # =========================
    # 📅 WEEKLY DATA (DYNAMIC)
    four_weeks_ago = now - timedelta(weeks=4)

    weekly_qs = (
        SuperReport.objects
        .filter(generated_date__gte=four_weeks_ago)
        .annotate(week=TruncWeek('generated_date'))
        .values('week')
        .annotate(count=Count('id'))
        .order_by('week')
    )

    weekly_data = [0, 0, 0, 0]
    weekly_labels = ["W1", "W2", "W3", "W4"]

    for i, item in enumerate(list(weekly_qs)[:4]):
        weekly_data[i] = item['count']

    # =========================
    # 📊 MONTHLY DATA (DYNAMIC)
    # =========================
    monthly_qs = (
        SuperReport.objects
        .annotate(month=TruncMonth('generated_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    monthly_labels = []
    monthly_data = []

    for item in monthly_qs:
        monthly_labels.append(item['month'].strftime("%b"))
        monthly_data.append(item['count'])


    category_qs = (
        TrainingProgram.objects
        .values('category')
        .annotate(count=Count('id'))
    )

    category_labels = []
    category_data = []

    for item in category_qs:
        category_labels.append(item['category'])
        category_data.append(item['count'])

    # =========================
    # 🔔 ALERTS
    # =========================
    critical_alerts = Alert.objects.filter(
        alert_type='Critical',
        is_read=False
    ).count()

    recent_alerts = Alert.objects.order_by('-created_at')[:5]

    # =========================
    # 🔔 NOTIFICATIONS
    # =========================
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]

    # =========================
    # 📜 ACTIVITY LOGS
    # =========================
    recent_logs = ActivityLog.objects.select_related('user').order_by('-timestamp')[:5]

    # =========================
    # CONTEXT
    # =========================
    context = {
        # USERS
        'total_trainees': total_trainees,
        'total_trainers': total_trainers,
        'total_managers': total_managers,

        # PROGRAMS
        'active_programs': active_programs,
        'new_programs': new_programs,
        'completion_rate': completion_rate,

        # GROWTH
        'trainee_growth': trainee_growth,
        'trainer_growth': trainer_growth,
        'new_trainers': new_trainers,

        # CHARTS
        'weekly_labels': json.dumps(weekly_labels),
        'weekly_data': json.dumps(weekly_data),


        # ALERTS
        'critical_alerts': critical_alerts,
        'recent_alerts': recent_alerts,

        # NOTIFICATIONS
        'notifications': notifications,

        # LOGS
        'recent_logs': recent_logs,

        'weekly_labels': json.dumps(weekly_labels),
        'weekly_data': json.dumps(weekly_data),

        'category_labels': json.dumps(category_labels),
        'category_data': json.dumps(category_data),
    }

    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
@user_passes_test(is_manager)
def manager_dashboard(request):

    total_employees = User.objects.filter(role='Trainee').count()

    total_trainings = TrainingProgram.objects.count()

    # 🔥 IMPORTANT: prefetch enrollments (performance + fix)
    trainings = TrainingProgram.objects.prefetch_related('enrollments').all().order_by('-id')

    updated_trainings = []

    excellent = good = average = poor = 0
    total_progress = 0

    for training in trainings:

        training_count = training.enrollments.count()

        progress = min(round((training_count / 5) * 100), 100)

        if progress >= 80:
            status = "Excellent"
            excellent += 1

        elif progress >= 60:
            status = "Good"
            good += 1

        elif progress >= 40:
            status = "Average"
            average += 1

        else:
            status = "Poor"
            poor += 1

        total_progress += progress

        training.progress = progress
        training.status = status

        updated_trainings.append(training)

    # 🔥 SAFE AVG (no crash fix)
    avg_performance = round(total_progress / len(updated_trainings)) if updated_trainings else 0

    trainings_in_progress = len([t for t in updated_trainings if t.progress < 100])

    current_score = avg_performance

    upcoming_reviews = trainings_in_progress

    today = timezone.now().date()

    attendance_labels = []
    attendance_values = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)

        present_count = Attendance.objects.filter(
            date=day,
            status='Present'
        ).count()

        attendance_labels.append(day.strftime("%a"))
        attendance_values.append(present_count)

    context = {
        'total_employees': total_employees,
        'total_trainings': total_trainings,
        'trainings_in_progress': trainings_in_progress,
        'avg_performance': avg_performance,
        'current_score': current_score,
        'upcoming_reviews': upcoming_reviews,

        'trainings': updated_trainings,

        'excellent': excellent,
        'good': good,
        'average': average,
        'poor': poor,

        'attendance_labels': json.dumps(attendance_labels),
        'attendance_values': json.dumps(attendance_values),
    }

    return render(request, 'dashboard/manager_dashboard.html', context)
# ===============================
# TRAINER DASHBOARD
# ===============================
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
import json

@login_required
@user_passes_test(is_trainer)
def trainer_dashboard(request):

    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    active_courses = TrainingProgram.objects.count()

    starting_soon = Session.objects.filter(
        date__gte=today,
        date__lte=today + timedelta(days=7)
    ).count()

    total_trainees = CustomUser.objects.filter(role='Trainee').count()

    new_trainees = Enrollment.objects.filter(
        enrolled_at__gte=week_ago
    ).count()

    completed_sessions = Session.objects.filter(completed=True).count()
    pending_sessions = Session.objects.filter(completed=False).count()



    # 🔥 LINE CHART DATA (last 4 weeks)
    chart_labels = []
    chart_values = []

    for i in range(4):
        start = today - timedelta(days=(28 - i*7))
        end = start + timedelta(days=7)

        count = Session.objects.filter(
            date__gte=start,
            date__lt=end
        ).count()

        chart_labels.append(f"Week {i+1}")
        chart_values.append(count)

    # 🔥 COURSE PROGRESS
    # 🔥 COURSE PROGRESS
    courses = TrainingProgram.objects.all()
    course_progress = []

    for c in courses:
        total = Session.objects.filter(course=c).count()

        completed = Session.objects.filter(
            course=c,
            completed=True
        ).count()

        percent = int((completed / total) * 100) if total > 0 else 0

        course_progress.append({
            "name": c.title,
            "percent": percent
        })

    sessions = Session.objects.filter(
        date__gte=today
    ).order_by('date')[:5]

    last_month = today - timedelta(days=30)

    trainees_this_month = CustomUser.objects.filter(
        role='Trainee',
        date_joined__gte=last_month
    ).count()

    trainee_growth = trainees_this_month


    context = {
        'active_courses': active_courses,
        'starting_soon': starting_soon,
        'total_trainees': total_trainees,
        'new_trainees': new_trainees,
        'completed_sessions': completed_sessions,
        'pending_sessions': pending_sessions,
        'sessions': sessions,
        'chart_labels': json.dumps(chart_labels),
        'chart_values': json.dumps(chart_values),
        'course_progress': course_progress,
        'trainee_growth': trainee_growth,
    }

    return render(request, 'dashboard/trainer_dashboard.html', context)



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from smart.models import Enrollment
from trainee.models import Certificate
from datetime import date, timedelta
   # सुनिश्चित import आहे
from datetime import date, timedelta
from django.db.models import Avg
import json

@login_required
def trainee_dashboard(request):
    user = request.user

    enrollments = Enrollment.objects.filter(trainee=user).select_related('training')

    total_courses = enrollments.count()
    in_progress = enrollments.filter(status='In Progress').count()
    completed = enrollments.filter(status='Completed').count()

    overall_progress = enrollments.aggregate(avg=Avg('progress'))['avg'] or 0

    certificates = Certificate.objects.filter(user=user)
    total_certificates = certificates.count()
    pending_certificates = max(completed - total_certificates, 0)

    # ================================
    # ✅ WEEKLY STUDY HOURS (FIXED)
    # ================================
    today = date.today()

    weeks = []
    study_hours = []

    for i in range(3, -1, -1):
        start = today - timedelta(days=(i + 1) * 7)
        end = today - timedelta(days=i * 7)

        weeks.append(f"Week {4 - i}")

        attendance_records = Attendance.objects.filter(
            employee=user,
            date__range=[start, end]
        )

        total_hours = 0

        for a in attendance_records:
            if a.status == "Present":
                total_hours += 2
            elif a.status == "Leave":
                total_hours += 1

        study_hours.append(total_hours)

    # ✅ PIE CHART DATA
    user_distribution = [in_progress, completed]

    context = {
        'total_courses': total_courses,
        'in_progress': in_progress,
        'completed': completed,
        'overall_progress': round(overall_progress),
        'total_certificates': total_certificates,
        'pending_certificates': pending_certificates,

        'study_hours': sum(study_hours),

        # ✅ IMPORTANT
        'weekly_labels': json.dumps(weeks),
        'weekly_data': json.dumps(study_hours),
        'user_distribution': json.dumps(user_distribution),

        'courses': enrollments,
    }

    return render(request, 'dashboard/trainee_dashboard.html', context)
# ===============================
# ACTIVITY LOGS
# ===============================
@login_required
def activity_logs(request):
    logs = ActivityLog.objects.all().order_by('-timestamp')
    return render(request, 'dashboard/activity_logs.html', {'logs': logs})


def dashboard_base(request):
    return render(request, 'base_dashboard.html')







def can_view_users(user):
    if not user.is_authenticated:
        return False

    role = (user.role or "").strip().lower()

    return role in ['superadmin', 'admin', 'manager', 'trainer']


@login_required
@user_passes_test(can_view_users)
def all_users(request):
    users = CustomUser.objects.all().order_by('-date_joined')

    return render(request, 'dashboard/all_users.html', {
        'users': users
    })


# USERS BY ROLE
@login_required
@user_passes_test(can_view_users)
def users_by_role(request, role):
    users = CustomUser.objects.filter(role=role)

    return render(request, 'dashboard/all_users.html', {
        'users': users,
        'title': f'{role} List'
    })

from django.db.models import Q

@login_required
def enrollment_list(request):

    search_query = request.GET.get('search', '')

    enrollments = Enrollment.objects.select_related('trainee', 'training')

    # 🔍 SEARCH FILTER
    if search_query:
        enrollments = enrollments.filter(
            Q(trainee__username__icontains=search_query) |
            Q(training__title__icontains=search_query) |
            Q(status__icontains=search_query)
        )

    return render(request, 'dashboard/enrollment_list.html', {
        'enrollments': enrollments,
        'search_query': search_query
    })


# views.py
@login_required
def all_courses(request):
    courses = TrainingProgram.objects.all()
    return render(request, 'dashboard/all_courses.html', {'courses': courses})