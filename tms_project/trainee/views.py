from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from smart.models import TrainingProgram, Enrollment

from .models import Module, Lesson, LessonProgress
  # 🔥 MUST ADD


# ===========================
# 🧾 MY COURSES PAGE
# ===========================
@login_required
def my_courses(request):
    user = request.user

    enrollments = Enrollment.objects.filter(
        trainee=user
    ).select_related('training')

    course_data = []

    for enroll in enrollments:
        program = enroll.training

        course_data.append({
            "id": program.id,
            "title": program.title if hasattr(program, "title") else program.name,
            "instructor": "Admin",
            "duration": getattr(program, "duration", 0),
            "students": getattr(program, "enrolled_count", lambda: 0)(),
            "rating": 4.8,
            "progress": enroll.progress if hasattr(enroll, "progress") else 0,
            "status": enroll.status
        })

    return render(request, "trainee/my_courses.html", {
        "courses": course_data
    })

import json
# ===========================
# 📚 COURSE CONTENT PAGE
# ===========================
@login_required
def course_content(request, course_id):
    course = get_object_or_404(TrainingProgram, id=course_id)
    modules = course.modules.all().order_by('order')

    total_lessons = 0
    completed_lessons = 0

    for module in modules:
        lessons = module.lessons.all().order_by('order')
        total_lessons += lessons.count()

        for lesson in lessons:
            if LessonProgress.objects.filter(
                user=request.user,
                lesson=lesson,
                completed=True
            ).exists():
                completed_lessons += 1

    # ✅ progress calculate
    progress = int((completed_lessons / total_lessons) * 100) if total_lessons else 0

    # ✅ time spent (simple demo logic)
    time_spent = f"{completed_lessons * 20} mins"

    context = {
        'course': course,
        'modules': modules,
        'progress': progress,
        'completed_lessons': completed_lessons,
        'total_lessons': total_lessons,
        'time_spent': time_spent
    }

    return render(request, 'trainee/course_content.html', context)


# ===========================
# ✅ MARK LESSON COMPLETE
# ===========================

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from smart.models import Enrollment
from .models import Lesson, LessonProgress


# 🔥 reusable function
def calculate_progress(user, course):
    total = Lesson.objects.filter(module__course=course).count()

    completed = LessonProgress.objects.filter(
        user=user,
        lesson__module__course=course,
        completed=True
    ).count()

    return int((completed / total) * 100) if total else 0


# =========================
# ✅ MARK COMPLETE (FINAL)
# =========================
@login_required
def mark_complete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    # ✅ mark lesson complete
    LessonProgress.objects.update_or_create(
        user=request.user,
        lesson=lesson,
        defaults={
            'completed': True,
            'completed_at': timezone.now()
        }
    )

    course = lesson.module.course

    # 🔥 calculate progress (function वापर)
    progress = calculate_progress(request.user, course)

    # 🔥 update enrollment safely
    enrollment, created = Enrollment.objects.get_or_create(
        trainee=request.user,
        training=course
    )

    enrollment.progress = progress

    # ✅ auto status
    if progress == 100:
        enrollment.status = "Completed"
    else:
        enrollment.status = "In Progress"

    enrollment.save()

    return redirect('course_content', course_id=course.id)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Assignment
from datetime import date
from datetime import date
from smart.models import Enrollment

@login_required
def assignments(request):
    user = request.user

    # ✅ only enrolled courses
    enrolled_courses = Enrollment.objects.filter(
        trainee=user
    ).values_list('training', flat=True)

    assignments = Assignment.objects.filter(
        course__in=enrolled_courses
    )

    urgent = 0
    progress = 0
    completed = 0

    data = []

    for a in assignments:
        days_left = (a.due_date - date.today()).days

        if a.status == 'pending':
            urgent += 1
        elif a.status == 'progress':
            progress += 1
        elif a.status in ['submitted', 'graded']:
            completed += 1

        data.append({
            "id": a.id,
            "title": a.title,
            "course": a.course.title,
            "due": a.due_date,
            "days_left": days_left,
            "status": a.status,
            "grade": a.grade
        })

    return render(request, "trainee/assignments.html", {
        "assignments": data,
        "urgent": urgent,
        "progress": progress,
        "completed": completed
    })

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
import json

from .models import SkillProgress, StudyHour
# adjust if needed
from .models import Certificate      # adjust if needed
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
import json
from datetime import datetime

from .models import SkillProgress, StudyHour, Certificate
from smart.models import Enrollment


@login_required
def my_progress(request):
    user = request.user

    # =========================
    # COURSES DATA
    # =========================
    enrollments = Enrollment.objects.filter(trainee=user)

    progress_list = []

    for e in enrollments:
        p = calculate_progress(user, e.training)
        progress_list.append(p)

    avg_progress = sum(progress_list) / len(progress_list) if progress_list else 0
    total_courses = enrollments.count()

    # =========================
    # CERTIFICATES
    # =========================
    certificates = Certificate.objects.filter(user=user).count()

    # =========================
    # STUDY HOURS (MONTHLY)
    # =========================
    study_data = StudyHour.objects.filter(user=user).order_by('month')

    months = []
    hours = []

    for s in study_data:
        m = s.month

        # ---- convert month safely ----
        if isinstance(m, str):
            for fmt in ("%Y-%m", "%B %Y", "%Y-%m-%d"):
                try:
                    m = datetime.strptime(m, fmt)
                    break
                except:
                    continue

        months.append(m.strftime("%b"))
        hours.append(s.hours)

    total_hours = sum(hours)

    # =========================
    # STREAK
    # =========================
    streak = 0
    for h in reversed(hours):
        if h > 0:
            streak += 1
        else:
            break

    # =========================
    # SKILLS
    # =========================
    skills = SkillProgress.objects.filter(user=user)

    context = {
        "avg_progress": round(avg_progress),
        "certificates": certificates,
        "total_hours": total_hours,
        "streak": streak,
        "skills": skills,
        "total_courses": total_courses,

        # Chart data
        "months": json.dumps(months),
        "hours": json.dumps(hours),
    }

    return render(request, "trainee/my_progress.html", context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Certificate
from smart.models import Enrollment   # progress साठी

@login_required
def my_certificates(request):
    user = request.user

    # Earned certificates
    earned = Certificate.objects.filter(user=user)

    # Pending (enrolled but no certificate yet)
    enrollments = Enrollment.objects.filter(trainee=user)

    pending = []
    for e in enrollments:
        if not Certificate.objects.filter(user=user, training=e.training).exists():
            pending.append({
                "course_name": e.training.title,
                "instructor": "Trainer",
                "progress": e.progress
            })

    context = {
        "earned": earned,
        "pending": pending,
        "earned_count": earned.count(),
        "pending_count": len(pending),
    }

    return render(request, "trainee/certificates.html", context)


def start_assignment(request, id):
    a = get_object_or_404(Assignment, id=id)
    a.status = "progress"
    a.save()
    return redirect('assignments')



@login_required
def view_assignment(request, id):
    a = get_object_or_404(Assignment, id=id)
    questions = Question.objects.filter(assignment=a)

    if request.method == "POST":
        for q in questions:
            ans = request.POST.get(f"answer_{q.id}")

            if ans:
                Answer.objects.create(
                    trainee=request.user,
                    question=q,
                    answer_text=ans
                )

        a.status = "submitted"
        a.save()

        return redirect("assignments")

    return render(request, "trainee/view_assignment.html", {
        "a": a,
        "questions": questions
    })

from trainer.models import Material   # 🔥 import


@login_required
def materials(request):
    user = request.user

    enrolled_courses = Enrollment.objects.filter(
        trainee=user
    ).values_list('training_id', flat=True)

    materials = Material.objects.filter(
        training_id__in=list(enrolled_courses)
    )

    return render(request, "trainee/materials.html", {
        "materials": materials
    })