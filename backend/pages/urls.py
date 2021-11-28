from django.urls import path
from .views import HomePageView, AboutPageView, UserHomeView

urlpatterns = [
    path('userhome/', UserHomeView.as_view(), name='userhome'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('', HomePageView.as_view(), name='home'),
]
