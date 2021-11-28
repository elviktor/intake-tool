from django.shortcuts import render
from django.views.generic import TemplateView
from intakemanager.models import IntakeUser

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'about.html'

class UserHomeView(TemplateView):
    template_name = 'intakemanager/userhome.html'
    def get_context_data(self,*args, **kwargs):
        context = super(UserHomeView, self).get_context_data(*args,**kwargs)
        context['users'] = IntakeUser.objects.all()
        return context
