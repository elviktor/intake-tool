from django.shortcuts import render
from .models import IntakeUser
from .forms import IntakeUserForm

def intakeUserForm(request):
    form = IntakeUserForm(data=request.POST, request=request)
    if form.is_valid():
        u = form.save()
        users = IntakeUser.objects.all()
        return render(request, 'intakemanager/userhome.html')
        # Change to render(request, 'intakemanager/userhome.html')

    else:
        form_class = IntakeUserForm(request=request)

    return render(request, 'intakemanager/intakeuser_form.html', {
        'form': form_class,
    })
