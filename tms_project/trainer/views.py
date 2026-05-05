from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Avg, Count, Max, Min

from .models import  Content,  Material, Progress
from django.shortcuts import render
from smart.models import TrainingProgram




def my_trainings(request):
    # Fetch all training programs for the trainer
    trainings = TrainingProgram.objects.all().order_by('-id')

    # Add a progress field for front-end
    for t in trainings:
        t.progress = min(round((t.completed_sessions / t.total_sessions) * 100), 100) if t.total_sessions else 0

    return render(request, "trainer/my_trainings.html", {"trainings": trainings})


# =========================
# 📘 CONTENT
# =========================
def create_content(request):
    courses = TrainingProgram.objects.all()   # or Course model

    if request.method == "POST":
        Content.objects.create(
            title=request.POST.get("title"),
            course_id=request.POST.get("course"),  # IMPORTANT FIX
            category=request.POST.get("category"),
            description=request.POST.get("description"),

            duration=request.POST.get("duration"),
            difficulty=request.POST.get("difficulty"),
            content_type=request.POST.get("content_type"),
            file=request.FILES.get("file"),
        )
        messages.success(request, "Content saved successfully!")
        return redirect("content_list")

    return render(request, "trainer/create_content.html", {
        "courses": courses
    })


def content_list(request):
    contents = Content.objects.all().order_by("-id")
    return render(request, "trainer/content_list.html", {"contents": contents})


# =========================
# 📚 COURSE
# =========================

def course_list(request):
    if request.method == "POST":
        TrainingProgram.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description")
        )
        return redirect("course_list")

    courses = TrainingProgram.objects.all().order_by("-id")
    return render(request, "trainer/course_list.html", {"courses": courses})


def delete_course(request, id):
    course = get_object_or_404(TrainingProgram, id=id)
    course.delete()
    return redirect("course_list")


def create_course(request):
    if request.method == "POST":
        TrainingProgram.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description")
        )
        return redirect("course_list")

    return render(request, "trainer/create_course.html")


# =========================
# 🎓 TRAININGS
# =========================



def add_training(request):
    if request.method == "POST":
        TrainingProgram.objects.create(
            title=request.POST.get("title"),
            trainees=request.POST.get("trainees"),
            sessions=request.POST.get("sessions"),
            next_date=request.POST.get("next_date"),
            progress=request.POST.get("progress"),
        )
        return redirect("my_trainings")

    return render(request, "trainer/add_trainings.html")


# =========================
# 📂 MATERIALS
# =========================

def material_list(request):
    materials = Material.objects.all()
    return render(request, "trainer/material_list.html", {"materials": materials})


def add_material(request):
    if request.method == "POST":
        Material.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            file=request.FILES.get("file"),
        )
        return redirect("material_list")

    return render(request, "trainer/add_material.html")


def edit_material(request, id):
    material = get_object_or_404(Material, id=id)

    if request.method == "POST":
        material.title = request.POST.get("title")
        material.description = request.POST.get("description")

        if request.FILES.get("file"):
            material.file = request.FILES.get("file")

        material.save()
        return redirect("material_list")

    return render(request, "trainer/edit_material.html", {"material": material})


def delete_material(request, id):
    material = get_object_or_404(Material, id=id)
    material.delete()
    return redirect("material_list")

from smart.models import TrainingProgram

def upload_material(request):
    courses = TrainingProgram.objects.all()

    if request.method == "POST":
        Material.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            file=request.FILES.get("file"),
            training_id=request.POST.get("training")   # ✅ THIS LINE IS KEY
        )
        return redirect("upload_material")

    return render(request, "trainer/upload_material.html", {
        "courses": courses
    })


# =========================
# 📊 PROGRESS
# =========================
from django.shortcuts import render
from django.db.models import Avg, Max, Min
from .models import Progress

def progress_view(request):
    from accounts.models import CustomUser
    from smart.models import TrainingProgram
    from .models import Progress
    from django.db.models import Avg, Max, Min

    trainees = CustomUser.objects.filter(role='Trainee')
    trainings = TrainingProgram.objects.all()

    for trainee in trainees:
        for training in trainings:
            Progress.objects.get_or_create(
                trainee=trainee,
                training=training,
                defaults={
                    "percentage": 75,
                    "completed_assignments": 7,
                    "total_assignments": 10,
                    "quiz_score": 80,
                    "attendance_percentage": 85
                }
            )

    progress = Progress.objects.select_related(
        "trainee", "training"
    ).all().order_by("-percentage")

    avg_progress = progress.aggregate(avg=Avg("percentage"))["avg"] or 0
    top_performers = progress.filter(percentage__gte=90).count()
    need_attention = progress.filter(percentage__lt=70).count()

    highest = progress.aggregate(max=Max("percentage"))["max"] or 0
    lowest = progress.aggregate(min=Min("percentage"))["min"] or 0

    context = {
        "progress": progress,
        "avg_progress": round(avg_progress, 1),
        "top_performers": top_performers,
        "need_attention": need_attention,
        "highest": highest,
        "lowest": lowest,
    }

    return render(request, "trainer/progress.html", context)


from trainee.models import Assignment
from smart.models import TrainingProgram
from django.contrib import messages

from trainer.models import Question

def create_assignment(request):
    courses = TrainingProgram.objects.all()

    if request.method == "POST":
        assignment = Assignment.objects.create(
            title=request.POST.get("title"),
            course_id=request.POST.get("course"),
            due_date=request.POST.get("due_date"),
            status="pending"
        )

        # ✅ SAVE QUESTIONS
        questions = request.POST.getlist("questions[]")

        for q in questions:
            if q.strip():
                Question.objects.create(
                    assignment=assignment,
                    text=q
                )

        messages.success(request, "Assignment + Questions created ✅")
        return redirect("assignment_list")

    return render(request, "trainer/create_assignment.html", {
        "courses": courses
    })

def assignment_list(request):
    assignments = Assignment.objects.select_related("course").order_by("-id")
    return render(request, "trainer/assignment_list.html", {
        "assignments": assignments
    })


