from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from smart.models import TrainingProgram


# Training List
@login_required
def training_list(request):
    trainings = TrainingProgram.objects.all()
    return render(request, 'trainings/training_list.html', {
        'trainings': trainings
    })


# Add Training
@login_required
def add_training(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        trainer_name = request.POST.get('trainer_name')
        duration = request.POST.get('duration')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Save Training
        TrainingProgram.objects.create(
            title=title,
            description=description,
            trainer_name=trainer_name,
            duration=duration,
            start_date=start_date,
            end_date=end_date
        )

        # Role-wise Redirect after Add Training
        if request.user.role == "Admin":
            return redirect('/dashboard/adminapp/')
        elif request.user.role == "Manager":
            return redirect('/dashboard/manager/')

        else:
            return redirect('/')

    return render(request, 'trainings/training_add.html')

def courses(request):
    return render(request, 'courses.html')