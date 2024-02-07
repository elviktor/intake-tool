from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import TTStorageBatchForm
from .models import Book, Strain, TT_Inventory, TT_Location, TT_Plant_Batch, TT_Plant_Batch_Harvest, TT_Storage_Batch,TT_Product_Batch, TT_Sublot, TT_Lab_Sample, Plant, Weight, Derivative, Plant_Harvest, Lab_Result, Lab_Sample_Result, Lab_Sample, Inventory, Inventory_Room, Inventory_Sublot, Inventory_Move, Plant_Cure, Invoice_Inventory, Invoice_Model, Manifest_Driver, Stop_Item, Manifest_Stop, Manifest_Vehicle, Manifest_ThirdPartyTransporter, Manifest, Grow_Room

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


class TTStorageBatchDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = TT_Storage_Batch

#https://stackoverflow.com/questions/53742129/how-do-you-modify-form-data-before-saving-it-while-using-djangos-createview

def store_produce(request, uid):
    storage_batch = TT_Storage_Batch.objects.get(pk=uid)

    if request.method == 'POST':
        form = TTStorageBatchForm(request.POST, instance=storage_batch)
        if form.is_valid():
            weight = form.cleaned_data['weight'] 
            harvest_batch = storage_batch.harvest_batch
            harvest_batch.remaining_dry_weight -= weight
            harvest_batch.save()
            form.save()
            return redirect('home')
    else:
        form = TTStorageBatchForm(instance=storage_batch)

    return render(request, 'store_produce.html', {'form': form, 'storage_batch': storage_batch})



class TTStorageBatchCreateView(LoginRequiredMixin,CreateView):
    form_class = TTStorageBatchForm
    template_name = 'tracker/tt_storage_batch_form.html'
    success_url = "home"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.weight_transfer()
        return super().form_valid(form)
    

class TTProductBatchDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = TT_Product_Batch


class TTSublotDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = TT_Sublot


class TTLabSampleDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = TT_Lab_Sample


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



