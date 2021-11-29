from django.urls import path
from .views import HomePageView, AboutPageView, UserHomeView, IntakeToolView

urlpatterns = [
    path('intaketool/', IntakeToolView.as_view(), name='intaketool'),
    path('userhome/', UserHomeView.as_view(), name='userhome'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('', HomePageView.as_view(), name='home'),
]
