
from django.contrib.auth.decorators import login_required


from accounts.models import CustomUser



# ✅ Admin Dashboard
@login_required
def admin_dashboard(request):
    return render(request, 'smart/admin_dashboard.html')


# ==============================
# 👨‍💼 MANAGERS
# ==============================

@login_required
def manage_managers(request):
    search_query = request.GET.get('search', '')

    managers = CustomUser.objects.filter(role="Manager")

    if search_query:
        managers = managers.filter(
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    return render(request, 'smart/manage_managers.html', {
        'managers': managers,
        'search_query': search_query
    })

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser


@login_required
def add_manager(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 🔍 Validation
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "❌ Username already exists")
            return render(request, 'smart/add_manager.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "❌ Email already exists")
            return render(request, 'smart/add_manager.html')

        # ✅ Create Manager
        CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            full_name=full_name,
            role="Manager"
        )

        messages.success(request, "✅ Manager added successfully")
        return redirect('manage_managers')

    return render(request, 'smart/add_manager.html')
@login_required
def edit_manager(request, id):
    manager = get_object_or_404(CustomUser, id=id, role="Manager")

    if request.method == "POST":
        manager.full_name = request.POST.get('full_name')
        manager.email = request.POST.get('email')
        manager.save()
        return redirect('manage_managers')

    return render(request, 'smart/edit_manager.html', {'manager': manager})


@login_required
def delete_manager(request, id):
    manager = get_object_or_404(CustomUser, id=id, role="Manager")
    manager.delete()
    return redirect('manage_managers')


# ==============================
# 👨‍🏫 TRAINERS
# ==============================

@login_required
def manage_trainers(request):
    search_query = request.GET.get('search', '')

    trainers = CustomUser.objects.filter(role='Trainer')

    if search_query:
        trainers = trainers.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    return render(request, 'smart/manage_trainers.html', {
        'trainers': trainers,
        'search_query': search_query
    })


@login_required
def add_trainer(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('add_trainer')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('add_trainer')

        CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            full_name=full_name,
            role="Trainer"
        )

        messages.success(request, "Trainer added successfully ✅")
        return redirect('manage_trainers')

    return render(request, 'smart/add_trainer.html')


# ==============================
# 👨‍🎓 TRAINEES (REAL DATA)
# ==============================
@login_required
def manage_trainees(request):
    search_query = request.GET.get('search', '')

    trainees = CustomUser.objects.filter(role='Trainee')

    # 🔍 Search
    if search_query:
        trainees = trainees.filter(
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    trainee_list = []

    for t in trainees:
        enrollments = Enrollment.objects.filter(trainee=t)

        # ✅ CASE 1: No enrollment (NEW trainee)
        if not enrollments.exists():
            trainee_list.append({
                'id': t.id,
                'name': t.full_name,
                'email': t.email,
                'initial': (t.full_name[:2].upper() if t.full_name else "NA"),
                'program': "Not Assigned",
                'progress': 0,
                'status': "Not Started"
            })

        # ✅ CASE 2: Has enrollment
        else:
            for e in enrollments:
                trainee_list.append({
                    'id': t.id,
                    'name': t.full_name,
                    'email': t.email,
                    'initial': (t.full_name[:2].upper() if t.full_name else "NA"),
                    'program': e.training.title,
                    'progress': e.progress,
                    'status': e.status
                })

    return render(request, 'smart/manage_trainees.html', {
        'trainees': trainee_list,
        'search_query': search_query
    })
# ==============================
# 📚 TRAINING PROGRAMS (DB BASED)
# ==============================
from datetime import date

from django.contrib.auth.decorators import login_required

from .models import TrainingProgram


@login_required
def training_programs(request):

    today = date.today()   # ✅ current date

    programs = TrainingProgram.objects.annotate(
        enrolled=Count('enrollments')
    )

    program_list = []

    for p in programs:
        percent = 0
        if p.capacity > 0:
            percent = int((p.enrolled / p.capacity) * 100)

        # ✅ FIXED STATUS LOGIC
        status = "Active" if p.start_date <= today else "Upcoming"

        program_list.append({
            'id': p.id,
            'name': p.title,
            'category': p.category,
            'duration': p.duration,
            'start_date': p.start_date,
            'enrolled': p.enrolled,
            'capacity': p.capacity,
            'status': status,
            'percent': percent
        })

    return render(request, 'smart/training_programs.html', {
        'programs': program_list
    })

from accounts.models import CustomUser  # adjust if needed

def edit_manager(request, id):
    manager = get_object_or_404(CustomUser, id=id, role='Manager')

    if request.method == "POST":
        manager.full_name = request.POST.get('full_name')
        manager.username = request.POST.get('username')
        manager.email = request.POST.get('email')

        password = request.POST.get('password')

        if password:
            manager.set_password(password)  # 🔐 hashed password

        manager.save()

        messages.success(request, "Manager updated successfully ✅")
        return redirect('manage_managers')  # change to your URL name

    return render(request, 'smart/edit_manager.html', {'manager': manager})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from accounts.models import CustomUser

def edit_trainer(request, id):
    trainer = get_object_or_404(CustomUser, id=id, role='Trainer')

    if request.method == "POST":
        trainer.full_name = request.POST.get('full_name')
        trainer.username = request.POST.get('username')
        trainer.email = request.POST.get('email')

        password = request.POST.get('password')

        if password:
            trainer.set_password(password)

        trainer.save()

        messages.success(request, "Trainer updated successfully ✅")
        return redirect('manage_trainers')  # your list page

    return render(request, 'smart/edit_trainer.html', {'trainer': trainer})

def delete_trainer(request, id):
    trainer = get_object_or_404(CustomUser, id=id, role='Trainer')

    trainer.delete()

    messages.success(request, "Trainer deleted successfully 🗑️")
    return redirect('manage_trainers')


@login_required
def add_trainee(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validation
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists ❌")
            return redirect('add_trainee')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists ❌")
            return redirect('add_trainee')

        # Create Trainee
        CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            full_name=full_name,
            role="Trainee"
        )

        messages.success(request, "Trainee added successfully ✅")
        return redirect('manage_trainees')

    return render(request, 'smart/add_trainee.html')

@login_required
def edit_trainee(request, id):
    trainee = get_object_or_404(CustomUser, id=id, role='Trainee')

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validation
        if CustomUser.objects.exclude(id=trainee.id).filter(username=username).exists():
            messages.error(request, "Username already exists ❌")
            return redirect('edit_trainee', id=id)

        if CustomUser.objects.exclude(id=trainee.id).filter(email=email).exists():
            messages.error(request, "Email already exists ❌")
            return redirect('edit_trainee', id=id)

        trainee.full_name = full_name
        trainee.username = username
        trainee.email = email

        if password:
            trainee.set_password(password)

        trainee.save()

        messages.success(request, "Trainee updated successfully ✅")
        return redirect('manage_trainees')

    return render(request, 'smart/edit_trainee.html', {'trainee': trainee})


@login_required
def delete_trainee(request, id):
    trainee = get_object_or_404(CustomUser, id=id, role='Trainee')

    if request.method == "POST":
        trainee.delete()
        messages.success(request, "Trainee deleted successfully 🗑️")
        return redirect('manage_trainees')

    return render(request, 'smart/delete_trainee.html', {'trainee': trainee})

@login_required
def add_program(request):
    if request.method == "POST":
        title = request.POST.get('title')
        category = request.POST.get('category')
        duration = request.POST.get('duration')
        start_date = request.POST.get('start_date')
        capacity = request.POST.get('capacity')

        TrainingProgram.objects.create(
            title=title,
            category=category,
            duration=duration,
            start_date=start_date,
            capacity=capacity
        )

        messages.success(request, "Program created successfully ✅")
        return redirect('training_programs')

    return render(request, 'smart/add_program.html')

@login_required
def edit_program(request, id):
    program = get_object_or_404(TrainingProgram, id=id)

    if request.method == "POST":
        program.title = request.POST.get('title')
        program.category = request.POST.get('category')
        program.duration = request.POST.get('duration')
        program.start_date = request.POST.get('start_date')
        program.capacity = request.POST.get('capacity')

        program.save()

        messages.success(request, "Program updated successfully ✅")
        return redirect('training_programs')

    return render(request, 'smart/edit_program.html', {'program': program})


@login_required
def delete_program(request, id):
    program = get_object_or_404(TrainingProgram, id=id)

    if request.method == "POST":
        program.delete()
        messages.success(request, "Program deleted successfully 🗑️")
        return redirect('training_programs')

    return render(request, 'smart/delete_program.html', {'program': program})


from django.shortcuts import render, get_object_or_404

@login_required
def program_detail(request, id):
    program = get_object_or_404(TrainingProgram, id=id)

    enrollments = Enrollment.objects.filter(training=program)

    return render(request, 'smart/program_detail.html', {
        'program': program,
        'enrollments': enrollments
    })


import json
from django.db.models import Count, Avg, Q
from django.db.models.functions import TruncDate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from .models import Enrollment


@login_required
def admin_reports(request):

    enrollments = Enrollment.objects.select_related('trainee', 'training')

    # =========================
    # 📊 STATS
    # =========================
    total_enrollments = enrollments.count()
    completions = enrollments.filter(status="Completed").count()

    avg_completion = enrollments.aggregate(avg=Avg('progress'))['avg'] or 0
    avg_completion = round(avg_completion, 1)

    # =========================
    # 📈 DAILY DATA (LAST 7 DAYS DYNAMIC)
    # =========================
    today = timezone.now().date()

    daily_qs = (
        enrollments
        .annotate(day=TruncDate('enrolled_at'))
        .values('day')
        .annotate(
            total=Count('id'),
            completed=Count('id', filter=Q(status="Completed"))
        )
        .order_by('day')
    )

    # convert to dict for fast lookup
    data_map = {
        item["day"]: item for item in daily_qs if item["day"]
    }

    labels = []
    total_data = []
    completed_data = []

    # last 7 days rolling (dynamic growth)
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)

        labels.append(day.strftime("%a"))  # Mon, Tue...

        day_data = data_map.get(day)

        if day_data:
            total_data.append(day_data["total"])
            completed_data.append(day_data["completed"])
        else:
            total_data.append(0)
            completed_data.append(0)

    # =========================
    # 📄 STATIC REPORTS
    # =========================
    reports = [

    ]

    context = {
        "total_enrollments": total_enrollments,
        "completions": completions,
        "avg_completion": avg_completion,

        # JSON safe for JS
        "labels": json.dumps(labels),
        "total_data": json.dumps(total_data),
        "completed_data": json.dumps(completed_data),

        "reports": reports,
    }

    return render(request, "smart/admin_reports.html", context)

from .models import AdminNotification
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def admin_notifications(request):
    user = request.user

    notifications = AdminNotification.objects.filter(
        Q(role__iexact=user.role) |
        Q(role__isnull=True)
    ).order_by('-created_at')

    unread_count = notifications.filter(is_read=False).count()

    return render(request, 'smart/admin_notification.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })


@login_required
def admin_mark_read(request, id):
    user = request.user

    notif = AdminNotification.objects.filter(
        Q(id=id),
        Q(role__iexact=user.role) | Q(role__isnull=True)
    ).first()

    if notif:
        notif.is_read = True
        notif.save()

    return redirect('admin_notification')


@login_required
def admin_delete_notification(request, id):
    user = request.user

    notif = AdminNotification.objects.filter(
        Q(id=id),
        Q(role__iexact=user.role) | Q(role__isnull=True)
    ).first()

    if notif:
        notif.delete()

    return redirect('admin_notification')


@login_required
def admin_mark_all_read(request):
    user = request.user

    AdminNotification.objects.filter(
        Q(role__iexact=user.role) | Q(role__isnull=True),
        is_read=False
    ).update(is_read=True)

    return redirect('admin_notification')