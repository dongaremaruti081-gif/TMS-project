from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser,  Notification
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dashboard.models import ActivityLog
from django.views.decorators.csrf import csrf_exempt
from smart.models import TrainingProgram



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import get_messages
from django.db.models import Avg
import re
from django.views.decorators.csrf import csrf_exempt
from accounts.models import TrainingManager
from .models import Attendance, Notification, Report, TeamSkillAssessment
from .models import Noti


User = get_user_model()


# 🏠 Home
# 🏠 Home
def home(request):
    return render(request, 'accounts/home.html')
def blog(request):
    return render(request, 'blog.html')
def linkedin(request):
    return render(request, 'linkedin.html')
def facebook(request):
    return render(request, 'facebook.html')
def about(request):
    return render(request, 'about.html')
def careers(request):
    return render(request, 'careers.html')
def features(request):
    return render(request, 'features.html')
def services(request):
    return render(request, 'services.html')
def contact(request):
    return render(request, 'contact.html')

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
from django.http import JsonResponse
@csrf_exempt
def register_view(request):
    if request.method == "POST":

        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        errors = {}

        # VALIDATIONS
        if not full_name:
            errors['full_name'] = "Full name is required"

        if not username:
            errors['username'] = "Username is required"
        elif len(username) < 4:
            errors['username'] = "Minimum 4 characters required"
        elif CustomUser.objects.filter(username=username).exists():
            errors['username'] = "Username already exists"

        if not email:
            errors['email'] = "Email is required"
        elif CustomUser.objects.filter(email=email).exists():
            errors['email'] = "Email already exists"

        if not phone:
            errors['phone'] = "Phone number is required"
        else:
            phone = phone.strip()
            if not phone.isdigit():
                errors['phone'] = "Only digits allowed (0-9)"
            elif len(phone) != 10:
                errors['phone'] = "Phone number must be exactly 10 digits"

        if not password:
            errors['password'] = "Password is required"
        elif len(password) < 6:
            errors['password'] = "Minimum 6 characters required"

        if password != confirm_password:
            errors['confirm_password'] = "Passwords do not match"

        if not role:
            errors['role'] = "Please select role"

        # ❌ ERROR CASE
        if errors:
            return render(request, 'accounts/register.html', {
                'errors': errors,
                'data': request.POST
            })

        # ✅ CREATE USER
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            role=role,
            full_name=full_name,
            email=email,
            phone=phone
        )

        # ✅ Notification
        superadmins = CustomUser.objects.filter(role="SuperAdmin")

        for admin in superadmins:
            Notification.objects.create(
                user=admin,
                title="New User Registered",
                message=f"{user.full_name} registered as {user.role}",
                is_read=False
            )

        return redirect('login')

    return render(request, 'accounts/register.html')


@csrf_exempt
def login_view(request):
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Activity log
            ActivityLog.objects.create(
                user=user,
                action=f"{user.role} {user.username} logged in"
            )

            # Notification
            Notification.objects.create(
                user=user,
                title="Login Successful",
                message="User logged in successfully",
                notification_type="info"
            )

            return redirect('dashboard_redirect')

        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid Credentials'
            })

    return render(request, 'accounts/login.html')
# 🔥 MAIN ROLE BASED REDIRECT
@login_required
def dashboard_redirect(request):

    user = request.user

    if user.role == "SuperAdmin":
        return redirect('superadmin_dashboard')

    elif user.role == "Admin":
        return redirect('admin_dashboard')

    elif user.role == "Manager":
        return redirect('manager_dashboard')

    elif user.role == "Trainer":
        return redirect('trainer_dashboard')

    elif user.role == "Trainee":
        return redirect('trainee_dashboard')

    return redirect('home')


# 📋 Manage Admins
@login_required
def manage_admins(request):
    admins = CustomUser.objects.filter(role="Admin")
    return render(request, 'accounts/manage_admins.html', {'admins': admins})


# 🔄 Toggle Admin Status
@login_required
def toggle_admin_status(request, id):
    admin = get_object_or_404(CustomUser, id=id, role="Admin")

    admin.is_active = not admin.is_active
    admin.save()

    ActivityLog.objects.create(
        user=request.user,
        action=f"Changed status of adminapp: {admin.username}"
    )

    messages.success(request, "Admin status updated")
    return redirect('manage_admins')
@csrf_exempt
@login_required
def add_admin(request):
    if request.method == "POST":

        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        errors = {}

        # Validations
        if not full_name:
            errors['full_name'] = "Full name is required"

        if not username:
            errors['username'] = "Username is required"
        elif len(username) < 4:
            errors['username'] = "Minimum 4 characters required"
        elif CustomUser.objects.filter(username=username).exists():
            errors['username'] = "Username already exists"

        if not email:
            errors['email'] = "Email is required"
        elif CustomUser.objects.filter(email=email).exists():
            errors['email'] = "Email already exists"

        if not phone or not phone.isdigit() or len(phone) != 10:
            errors['phone'] = "Enter valid 10 digit phone"

        if not password:
            errors['password'] = "Password is required"
        elif len(password) < 6:
            errors['password'] = "Minimum 6 characters required"

        # ❌ ERROR CASE
        if errors:
            return render(request, 'accounts/add_admin.html', {
                "errors": errors,
                "data": request.POST
            })

        # ✅ CREATE ADMIN
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            full_name=full_name,
            email=email,
            phone=phone,
            role="Admin"
        )

        ActivityLog.objects.create(
            user=request.user,
            action=f"Added adminapp: {username}"
        )

        return redirect('manage_admins')

    return render(request, 'accounts/add_admin.html')

# ✏️ Edit Admin
@csrf_exempt
@login_required
def edit_admin(request, id):
    admin = get_object_or_404(CustomUser, id=id, role="Admin")

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        errors = {}

        if not full_name:
            errors["full_name"] = "Full name is required"

        if not email:
            errors["email"] = "Email is required"

        if not phone or not phone.isdigit() or len(phone) != 10:
            errors["phone"] = "Enter valid 10 digit phone"

        # ❌ ERROR CASE
        if errors:
            return render(request, 'accounts/edit_admin.html', {
                "errors": errors,
                "admin": admin
            })

        # ✅ UPDATE
        admin.full_name = full_name
        admin.email = email
        admin.phone = phone
        admin.save()

        ActivityLog.objects.create(
            user=request.user,
            action=f"Edited adminapp: {admin.username}"
        )

        return redirect('manage_admins')

    return render(request, 'accounts/edit_admin.html', {
        "admin": admin
    })


# ❌ Delete Admin

@login_required
@csrf_exempt
def delete_admin(request, id):
    admin = get_object_or_404(CustomUser, id=id, role="Admin")

    ActivityLog.objects.create(
        user=request.user,
        action=f"Deleted adminapp: {admin.username}"
    )

    admin.delete()

    messages.success(request, "Admin deleted successfully")
    return redirect('manage_admins')



# 👤 Profile
@login_required
@csrf_exempt
def profile_view(request):
    user = request.user

    if request.method == "POST":
        user.full_name = request.POST.get("full_name")
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")

        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES.get('profile_image')

        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    return render(request, "accounts/profile.html", {"user": user})


# 🔑 Change Password
@login_required
@csrf_exempt
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not request.user.check_password(current_password):
            messages.error(request, "Current password incorrect")
            return redirect("profile")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("profile")

        request.user.set_password(new_password)
        request.user.save()

        messages.success(request, "Password updated")
        return redirect("login")





from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Notification
@login_required
def notifications_view(request):

    user = request.user

    hierarchy = {
        "superadmin": 4,
        "admin": 3,
        "manager": 2,
        "trainer": 1,
        "trainee": 0,
    }

    user_role = (user.role or "").strip().lower()
    user_level = hierarchy.get(user_role, 0)

    notifications = Notification.objects.all().order_by('-created_at')

    filtered = []

    for n in notifications:

        notif_role = (n.role or "").strip().lower()

        # global notification
        if not notif_role:
            filtered.append(n)
            continue

        notif_level = hierarchy.get(notif_role, 0)

        if user_level >= notif_level:
            filtered.append(n)

    unread_count = sum(1 for n in filtered if not n.is_read)

    return render(request, "accounts/notifications.html", {
        "notifications": filtered,
        "unread_count": unread_count
    })
# ✅ Mark single notification as read
@login_required
@csrf_exempt
def mark_as_read(request, id):
    user = request.user

    def can_view(notif_role):
        if not notif_role:
            return True

        hierarchy = {
            "superadmin": 4,
            "admin": 3,
            "manager": 2,
            "trainer": 1,
            "trainee": 0,
        }

        user_level = hierarchy.get(user.role.lower(), 0)
        notif_level = hierarchy.get(notif_role.lower(), 0)

        return user_level >= notif_level

    notif = Notification.objects.filter(
        Q(id=id),
        Q(user=user) |
        Q(role__isnull=True)
    ).first()

    if notif and can_view(notif.role):
        notif.is_read = True
        notif.save()

    return redirect('notifications')


# ✅ Mark all notifications as read
@login_required
@csrf_exempt
def mark_all_read(request):
    user = request.user

    def can_view(notif_role):
        if not notif_role:
            return True

        hierarchy = {
            "superadmin": 4,
            "admin": 3,
            "manager": 2,
            "trainer": 1,
            "trainee": 0,
        }

        user_level = hierarchy.get(user.role.lower(), 0)
        notif_level = hierarchy.get(notif_role.lower(), 0)

        return user_level >= notif_level

    notifications = Notification.objects.filter(
        Q(user=user) |
        Q(role__isnull=True),
        is_read=False
    )

    for n in notifications:
        if can_view(n.role):
            n.is_read = True
            n.save()

    return redirect('notifications')


# 🗑️ Delete notification
@login_required
@csrf_exempt
def delete_notification(request, id):
    user = request.user

    def can_view(notif_role):
        hierarchy = {
            "superadmin": 4,
            "admin": 3,
            "manager": 2,
            "trainer": 1,
            "trainee": 0,
        }

        user_role = (user.role or "").strip().lower()
        notif_role = (notif_role or "").strip().lower()

        user_level = hierarchy.get(user_role, 0)
        notif_level = hierarchy.get(notif_role, 0)

        return user_level >= notif_level

    # 🔥 IMPORTANT: get notification
    notification = get_object_or_404(Notification, id=id)

    # 🔥 permission check (optional)
    if not can_view(notification.role):
        return redirect('notifications')   # or return 403

    # delete
    notification.delete()

    # 🔥 MUST RETURN HTTP RESPONSE
    return redirect('notifications')

from django.contrib.auth import logout

from django.http import JsonResponse
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')    


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from accounts.models import User
from smart.models import TrainingProgram, Enrollment
from .models import TrainingManager, Noti

@csrf_exempt
@login_required
def assign_training(request):

    employees = User.objects.filter(role='Trainee').order_by('full_name')
    trainers = User.objects.filter(role='Trainer').order_by('full_name')
    training_list = TrainingProgram.objects.all().order_by('-id')
    trainings = TrainingManager.objects.select_related('employee').all().order_by('-id')

    if request.method == "POST":

        employee_ids = request.POST.getlist('employees')   # ✅ MULTIPLE
        trainer_id = request.POST.get('trainer')
        training_id = request.POST.get('training')

        if not employee_ids or not trainer_id or not training_id:
            messages.error(request, "All fields required ❌")
            return redirect('assign_training')

        trainer = get_object_or_404(User, id=trainer_id, role='Trainer')
        training_obj = get_object_or_404(TrainingProgram, id=training_id)

        success_count = 0

        for emp_id in employee_ids:

            employee = get_object_or_404(User, id=emp_id, role='Trainee')

            # ✅ DEPARTMENT CHECK
            if employee.department != trainer.department:
                messages.warning(request, f"{employee.username} skipped (different dept)")
                continue

            # Save TrainingManager
            TrainingManager.objects.create(
                employee=employee,
                title=training_obj.title,
                trainer_name=trainer.full_name or trainer.username
            )

            # Enrollment
            enrollment, created = Enrollment.objects.get_or_create(
                trainee=employee,
                training=training_obj,
                defaults={
                    'progress': 0,
                    'status': 'In Progress'
                }
            )

            if created:
                success_count += 1

            # Notification
            Noti.objects.create(
                user=employee,
                title=f"Training Assigned: {training_obj.title}",
                message=f"You received new training",
                notification_type="info"
            )

        messages.success(request, f"{success_count} employees assigned ✅")

        return redirect('assign_training')

    return render(request, 'accounts/assign_training.html', {
        'employees': employees,
        'trainers': trainers,
        'trainings': trainings,
        'training_list': training_list
    })
# EMPLOYEE MANAGEMENT
# ======================================================
@csrf_exempt
@login_required
def employee_management(request):
    employees = User.objects.filter(role='Trainee').order_by('-id')

    return render(request, 'accounts/employee_management.html', {
        'employees': employees
    })


# ======================================================
# ADD EMPLOYEE
# ======================================================
@csrf_exempt
@login_required
def add_employee(request):
    if request.method == "POST":

        username = request.POST.get('username')
        phone = request.POST.get('phone')
        department = request.POST.get('department')

        if not re.match("^[A-Za-z]+$", username):
            return redirect('employee_management')

        if not phone.isdigit() or len(phone) != 10:
            return redirect('employee_management')

        if User.objects.filter(username=username).exists():
            return redirect('employee_management')

        User.objects.create_user(
            username=username,
            password=request.POST.get('password'),
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=phone,
            role=request.POST.get('role'),
            department=department
        )

        messages.success(request, "Employee Added Successfully ✅")

    return redirect('employee_management')


# ======================================================
# DELETE EMPLOYEE
# ======================================================
@csrf_exempt
@login_required
def delete_employee(request, id):
    employee = get_object_or_404(User, id=id)
    employee.delete()
    return redirect('employee_management')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import get_messages
from django.db.models import Avg
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Attendance
from django.contrib.auth import get_user_model
from smart.models import TrainingProgram
User = get_user_model()

def attendance_view(request):

    trainees = User.objects.filter(role='Trainee').order_by('full_name')
    trainings = TrainingProgram.objects.all().order_by('-id')

    # ✅ IMPORTANT FIX
    for t in trainees:
        t.training_ids = list(
            Enrollment.objects.filter(trainee=t)
            .values_list('training_id', flat=True)
        )

    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        training_id = request.POST.get('training')
        date = request.POST.get('date')
        status = request.POST.get('status')

        if not (employee_id and training_id and date and status):
            messages.error(request, "All fields are required ❌")
            return redirect('attendance')

        if Attendance.objects.filter(
            employee_id=employee_id,
            training_id=training_id,
            date=date
        ).exists():
            messages.warning(request, "Attendance already marked ⚠️")
            return redirect('attendance')

        employee = get_object_or_404(User, id=employee_id, role='Trainee')
        training = get_object_or_404(TrainingProgram, id=training_id)

        Attendance.objects.create(
            employee=employee,
            training=training,
            date=date,
            status=status
        )

        messages.success(request, "Attendance marked successfully ✅")
        return redirect('attendance')

    records = Attendance.objects.select_related('employee', 'training').order_by('-date')

    return render(request, 'accounts/attendance.html', {
        'trainees': trainees,
        'trainings': trainings,
        'records': records
    })

from django.http import JsonResponse
from .models import TrainingManager
from django.http import JsonResponse
from .models import TrainingManager

@login_required
def get_courses(request, emp_id):

    trainings = TrainingManager.objects.filter(
        employee_id=emp_id
    )

    data = []

    for t in trainings:
        data.append({
            "id": t.id,
            "title": t.title
        })

    return JsonResponse(data, safe=False)

import json
import re

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import get_messages
from django.db.models import Avg


from .models import Attendance, Notification, Report, TeamSkillAssessment

User = get_user_model()


# ======================================================
# REPORTS & ANALYTICS (FINAL CLEAN VERSION)
# ======================================================
@csrf_exempt
@login_required
def reports_analytics(request):

    employees_qs = User.objects.filter(role='Trainee')

    # ================= TOP CARDS =================
    team_members = employees_qs.count()

    total_attendance = Attendance.objects.count()
    present_attendance = Attendance.objects.filter(status='Present').count()

    attendance_rate = round(
        (present_attendance / total_attendance) * 100
    ) if total_attendance else 0

    training_hours = TrainingManager.objects.count() * 8

    # ================= EMPLOYEE TABLE =================
    employees = []

    excellent = good = average = poor = 0

    for emp in employees_qs:

        emp_total = Attendance.objects.filter(employee=emp).count()
        emp_present = Attendance.objects.filter(employee=emp, status='Present').count()

        emp_attendance = round(
            (emp_present / emp_total) * 100
        ) if emp_total else 0

        if emp_attendance >= 90:
            status = "Excellent"
            excellent += 1
        elif emp_attendance >= 70:
            status = "Good"
            good += 1
        elif emp_attendance >= 40:
            status = "Average"
            average += 1
        else:
            status = "Poor"
            poor += 1

        employees.append({
            "name": emp.full_name or emp.username,
            "department": emp.department or "N/A",
            "attendance": emp_attendance,
            "status": status
        })

    # ================= PIE CHART =================
    performance_data = [excellent, good, average, poor]

    # ================= DAY-WISE LINE CHART FIX =================
    from datetime import timedelta
    from django.utils import timezone

    today = timezone.now().date()

    attendance_labels = []
    attendance_values = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)

        count = Attendance.objects.filter(
            date=day,
            status='Present'
        ).count()

        attendance_labels.append(day.strftime("%a"))  # Mon, Tue
        attendance_values.append(count)

    # ================= CONTEXT (FIXED) =================
    return render(request, "accounts/reports_analytics.html", {
        "team_members": team_members,
        "attendance_rate": attendance_rate,
        "training_hours": training_hours,

        "employees": employees,
        "performance_data": performance_data,
        "attendance_labels": attendance_labels,
        "attendance_values": attendance_values,
    })
# PROFILE
# ======================================================
@csrf_exempt
@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":

        phone = request.POST.get('phone')

        if not phone.isdigit() or len(phone) != 10:
            return redirect('profile')

        user.full_name = request.POST.get('full_name')
        user.email = request.POST.get('email')
        user.phone = phone

        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES.get('profile_image')

        user.save()
        return redirect('profile')

    return render(request, 'accounts/profile.html')


# ======================================================
# CHANGE PASSWORD
# ======================================================
@csrf_exempt
@login_required
def change_password(request):

    if request.method == "POST":

        user = request.user

        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if user.check_password(current_password):

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)

    return redirect('profile')


# ======================================================
# NOTIFICATIONS
@login_required
def noti_view(request):

    filter_type = request.GET.get('filter', 'all')

    notifications = Noti.objects.filter(user=request.user).order_by('-created_at')

    if filter_type == 'unread':
        notifications = notifications.filter(is_read=False)

    elif filter_type == 'important':
        notifications = notifications.filter(notification_type='warning')

    unread_count = Noti.objects.filter(user=request.user, is_read=False).count()

    return render(request, 'accounts/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count,
        'active_tab': filter_type
    })