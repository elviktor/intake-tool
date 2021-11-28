from django.shortcuts import render
from .models import IntakeUser
from .forms import IntakeUserForm

def intakeUserForm(request):
    form = IntakeUserForm(request.POST)
    if form.is_valid():
        u = form.save()
        users = IntakeUser.objects.all()
        return render(request, 'home.html')

    else:
        form_class = IntakeUserForm

    return render(request, 'intakemanager/intakeuser_form.html', {
        'form': form_class,
    })
