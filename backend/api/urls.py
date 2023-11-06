from django.urls import path
from api.views import APIBookDetailView, api_book_list

urlpatterns = [
    path('books/<int:pk>/', APIBookDetailView.as_view()),
    path('books/', api_book_list),
]