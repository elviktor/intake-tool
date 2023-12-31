from django.urls import path
from .views import BookListView, PlantListView

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('', PlantListView.as_view(), name='plant_list'),
]