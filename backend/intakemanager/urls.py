from django.urls import path
from . import views

urlpatterns = [
    path('profile/intakeuserform', views.intakeUserForm, name='intakeuser_form'),
]
