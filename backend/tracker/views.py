from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import generic
from .models import Book, Plant, Strain, TT_Inventory, TT_Location, TT_Plant_Batch, TT_Plant_Batch_Harvest, TT_Product_Batch, TT_Sublot

class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'

class PlantListView(ListView):
    model = Plant
    template_name = 'plant_list.html'


class StrainDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Strain


class TTInventoryDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = TT_Inventory


class TTLocationDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = TT_Location


class TTPlantBatchDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = TT_Plant_Batch


class TTPlantBatchHarvestDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = TT_Plant_Batch_Harvest


class TTProductBatchDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = TT_Product_Batch


class TTSublotDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = TT_Sublot

