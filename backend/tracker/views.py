from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import generic
from .models import Book, Strain, TT_Inventory, TT_Location, TT_Plant_Batch, TT_Plant_Batch_Harvest, TT_Product_Batch, TT_Sublot, Plant, Weight, Derivative, Plant_Harvest, Lab_Result, Lab_Sample_Result, Lab_Sample, Inventory, Inventory_Room, Inventory_Sublot, Inventory_Move, Plant_Cure, Invoice_Inventory, Invoice_Model, Manifest_Driver, Stop_Item, Manifest_Stop, Manifest_Vehicle, Manifest_ThirdPartyTransporter, Manifest, Grow_Room

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


class PlantDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Plant


class WeightDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Weight



class DerivativeDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Derivative



class PlantHarvestDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Plant_Harvest



class LabResultDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Lab_Result



class LabSampleResultDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Lab_Sample_Result



class LabSampleDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Lab_Sample



class InventoryDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Inventory



class InventoryRoomDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Inventory_Room



class InventorySublotDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Inventory_Sublot



class InventoryMoveDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Inventory_Move



class PlantCureDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Plant_Cure



class InvoiceInventoryDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Invoice_Inventory



class InvoiceModelDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Invoice_Model



class ManifestDriverDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Manifest_Driver



class StopItemDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Stop_Item



class ManifestStopDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Manifest_Stop



class ManifestVehicleDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Manifest_Vehicle



class ManifestThirdPartyTransporterDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Manifest_ThirdPartyTransporter



class ManifestDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Manifest



class GrowRoomDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Grow_Room



