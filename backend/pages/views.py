from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from intakemanager.models import IntakeUser

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'about.html'

class UserHomeView(TemplateView):
    template_name = 'intakemanager/userhome.html'
    def get_context_data(self,*args, **kwargs):
        context = super(UserHomeView, self).get_context_data(*args,**kwargs)
        user = self.request.user
        intakeuser_single = get_object_or_404(IntakeUser, user=user)
        intakeuser_single_msc_group = intakeuser_single.msc_group
        context['msc_group'] = intakeuser_single
        return context

class IntakeToolView(TemplateView):
    template_name = 'intaketool/intaketool.html'
