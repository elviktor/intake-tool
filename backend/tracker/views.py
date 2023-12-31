from django.shortcuts import render
from django.views.generic import ListView
from .models import Book, Plant

class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'

class PlantListView(ListView):
    model = Plant
    template_name = 'plant_list.html'
