from django.urls import path
from api.views import APIBookDetailView, APIPlantDetailView, api_book_list, api_plant_list

urlpatterns = [
    path('books/<int:pk>/', APIBookDetailView.as_view()),
    path('books/', api_book_list),

    path('plants/<int:pk>/', APIPlantDetailView.as_view()),
    path('plants/', api_plant_list)
]