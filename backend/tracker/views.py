from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import generic, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from . import forms
from .models import Book, Strain, TT_Inventory, TT_Inventory_Product, TT_Location, TT_Plant_Batch, TT_Plant_Batch_Harvest, TT_Storage_Batch,TT_Product_Batch, TT_Sublot, TT_Lab_Sample, Plant, Weight, Derivative, Plant_Harvest, Lab_Result, Lab_Sample_Result, Lab_Sample, Inventory, Inventory_Room, Inventory_Sublot, Inventory_Move, Plant_Cure, Invoice_Inventory, Invoice_Model, Manifest_Driver, Stop_Item, Manifest_Stop, Manifest_Vehicle, Manifest_ThirdPartyTransporter, Manifest, Grow_Room, TT_Location_Delete,TT_Sublot_Delete,Strain_Delete,TT_Plant_Batch_Delete,TT_Plant_Batch_Harvest_Delete,TT_Storage_Batch_Delete,TT_Product_Batch_Delete,Lab_Result_Delete,Lab_Sample_Result_Delete,TT_Lab_Sample_Delete,TT_Inventory_Delete,TT_Inventory_Product_Delete,Invoice_Model_Delete,Invoice_Inventory_Delete, TT_User_Info

# Contents
# ========
# > TT Object Conversion Form Views
# > Create Update Delete Template Views
# > Detail Template Views
# > List Template Views


# TT Object Conversion Form Views
# ===============================

#https://stackoverflow.com/questions/53742129/how-do-you-modify-form-data-before-saving-it-while-using-djangos-createview

@login_required
def harvest_to_storage(request):
    #harvest_batch = TT_Plant_Batch_Harvest.objects.get(uid=pk)

    if request.method == 'POST':

        harvest_batch = None
        location = None
        sublot = None
        user = request.user

        form = forms.TTHarvestToStorageForm(request.POST, user=user)
        formset_a = forms.TTHarvestToStorageFormsetA(instance=harvest_batch, form_kwargs={'user': request.user})
        formset_b = forms.TTHarvestToStorageFormsetB(instance=location, form_kwargs={'user': request.user})
        formset_c = forms.TTHarvestToStorageFormsetC(instance=sublot, form_kwargs={'user': request.user})

        if form.is_valid():
            weight = form.cleaned_data['weight'] 
            wet_dry = form.cleaned_data['wet_dry']
            package_number = form.cleaned_data['package_number']
            harvest_batch = form.cleaned_data['harvest_batch']
            location = form.cleaned_data['location']
            sublot = form.cleaned_data['sublot'] 

            form = forms.TTHarvestToStorageForm(request.POST, instance=harvest_batch, user=user)
            formset_a = forms.TTHarvestToStorageFormsetA(instance=harvest_batch, form_kwargs={'user': request.user})
            formset_b = forms.TTHarvestToStorageFormsetB(instance=location, form_kwargs={'user': request.user})
            formset_c = forms.TTHarvestToStorageFormsetC(instance=sublot, form_kwargs={'user': request.user})

            # Create a new Product instance and associate it with the inventory
            storage_batch = TT_Storage_Batch.objects.create(user=request.user, harvest_batch=harvest_batch,location=location, sublot=sublot, weight=weight, package_number=package_number, wet_dry=wet_dry)

            if wet_dry == "wet":
                # Update the harvest batch weight
                harvest_batch.remaining_wet_weight -= weight
                harvest_batch.save()
                form.save()
            
            if wet_dry == "dry":
                # Update the harvest batch weight
                harvest_batch.remaining_dry_weight -= weight
                harvest_batch.save()
                form.save()
            
            return redirect('home')
    else:

        harvest_batch = None
        location = None
        sublot = None
        user = request.user

        form = forms.TTHarvestToStorageForm(user=user)
        formset_a = forms.TTHarvestToStorageFormsetA(instance=harvest_batch, form_kwargs={'user': request.user})
        formset_b = forms.TTHarvestToStorageFormsetB(instance=location, form_kwargs={'user': request.user})
        formset_c = forms.TTHarvestToStorageFormsetC(instance=sublot, form_kwargs={'user': request.user})

    return render(request, 'tracker/tt_harvest_to_storage_form.html', {'form': form})

@login_required
def storage_to_product(request):

    if request.method == 'POST':

        harvest_batch = None
        storage_batches = None
        location = None
        sublot = None
        user = request.user

        form = forms.TTStorageToProductForm(request.POST,user=user)
        formset_a = forms.TTStorageToProductFormsetA(instance=harvest_batch, form_kwargs={'user': request.user})
        formset_b = forms.TTStorageToProductFormsetB(instance=storage_batches, form_kwargs={'user': request.user})
        formset_c = forms.TTStorageToProductFormsetC(instance=location, form_kwargs={'user': request.user})
        formset_d = forms.TTStorageToProductFormsetD(instance=sublot, form_kwargs={'user': request.user})


        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            wet_dry = form.cleaned_data['wet_dry']
            storage_batches = form.cleaned_data['storage_batches']
            harvest_batch = form.cleaned_data['harvest_batch']
            location = form.cleaned_data['location']
            sublot = form.cleaned_data['sublot']
            total_weight = form.cleaned_data['total_weight']
            total_quantity = form.cleaned_data['total_quantity']

            form = forms.TTStorageToProductForm(request.POST, instance=user, user=user)
            formset_a = forms.TTStorageToProductFormsetA(instance=harvest_batch, form_kwargs={'user': request.user})
            formset_b = forms.TTStorageToProductFormsetB(instance=storage_batches, form_kwargs={'user': request.user})
            formset_c = forms.TTStorageToProductFormsetC(instance=location, form_kwargs={'user': request.user})
            formset_d = forms.TTStorageToProductFormsetD(instance=sublot, form_kwargs={'user': request.user})

            # Create a new instance
            product_batch = TT_Product_Batch.objects.create( user=request.user, product_name=product_name, harvest_batch=harvest_batch, storage_batches=storage_batches, location=location, sublot=sublot, total_weight=total_weight, remaining_weight=total_weight, total_quantity=total_quantity, remaining_quantity=total_quantity,  wet_dry=wet_dry)
            
            form.save()

            return redirect('home')
    else:
        harvest_batch = None
        storage_batches = None
        location = None
        sublot = None
        user = request.user

        form = forms.TTStorageToProductForm(user=user)
        formset_a = forms.TTStorageToProductFormsetA(instance=harvest_batch, form_kwargs={'user': request.user})
        formset_b = forms.TTStorageToProductFormsetB(instance=storage_batches, form_kwargs={'user': request.user})
        formset_c = forms.TTStorageToProductFormsetC(instance=location, form_kwargs={'user': request.user})
        formset_d = forms.TTStorageToProductFormsetD(instance=sublot, form_kwargs={'user': request.user})
        

    return render(request, 'tracker/tt_storage_to_product_form.html', {'form': form})

@login_required
def product_to_lab_sample(request):
    
    if request.method == 'POST':

        product_batch = None
        location = None
        sublot = None
        results = None
        test_results = None
        user = request.user

        form = forms.TTProductToLabSampleForm(request.POST,user=user)
        formset_a = forms.TTProductToLabSampleFormsetA(instance=product_batch, form_kwargs={'user': request.user})
        formset_b = forms.TTProductToLabSampleFormsetB(instance=location, form_kwargs={'user': request.user})
        formset_c = forms.TTProductToLabSampleFormsetC(instance=sublot, form_kwargs={'user': request.user})
        formset_d = forms.TTProductToLabSampleFormsetD(instance=results, form_kwargs={'user': request.user})
        formset_e = forms.TTProductToLabSampleFormsetE(instance=test_results, form_kwargs={'user': request.user})


        if form.is_valid():
            sample_name = form.cleaned_data['sample_name']
            amount = form.cleaned_data['amount'] 
            quantity = form.cleaned_data['quantity']
            product_batch = form.cleaned_data['product_batch']
            location = form.cleaned_data['location']
            sublot = form.cleaned_data['sublot'] 
            results = form.cleaned_data['results'] 
            test_results = form.cleaned_data['test_results'] 

            form = forms.TTProductToLabSampleForm(request.POST, instance=user, user=user)
            formset_a = forms.TTProductToLabSampleFormsetA(instance=product_batch, form_kwargs={'user': request.user})
            formset_b = forms.TTProductToLabSampleFormsetB(instance=location, form_kwargs={'user': request.user})
            formset_c = forms.TTProductToLabSampleFormsetC(instance=sublot, form_kwargs={'user': request.user})
            formset_d = forms.TTProductToLabSampleFormsetD(instance=results, form_kwargs={'user': request.user})
            formset_e = forms.TTProductToLabSampleFormsetE(instance=test_results, form_kwargs={'user': request.user})

            # Create a new Product instance and associate it with the inventory
            lab_sample_batch = TT_Lab_Sample.objects.create(user=request.user,sample_name=sample_name, product_batch=product_batch, location=location, sublot=sublot, amount=amount, quantity=quantity, results=results, test_results=test_results)

            # Update the product batch amount (weight) and quantity
            product_batch.remaining_weight -= amount
            product_batch.remaining_quantity -= quantity
            product_batch.save()
            form.save()
            
            return redirect('home')
    
    else:
        product_batch = None
        location = None
        sublot = None
        results = None
        test_results = None
        user = request.user

        form = forms.TTProductToLabSampleForm(user=user)
        formset_a = forms.TTProductToLabSampleFormsetA(instance=product_batch, form_kwargs={'user': request.user})
        formset_b = forms.TTProductToLabSampleFormsetB(instance=location, form_kwargs={'user': request.user})
        formset_c = forms.TTProductToLabSampleFormsetC(instance=sublot, form_kwargs={'user': request.user})
        formset_d = forms.TTProductToLabSampleFormsetD(instance=results, form_kwargs={'user': request.user})
        formset_e = forms.TTProductToLabSampleFormsetE(instance=test_results, form_kwargs={'user': request.user})

    return render(request, 'tracker/tt_product_to_lab_sample_form.html', {'form': form})

@login_required
def product_to_inventory(request):
    
    if request.method == 'POST':
        
        inventory = None
        product_batch = None
        user = request.user
        
        form = forms.TTProductToInventoryForm(request.POST,user=user)
        formset_a = forms.TTProductToInventoryFormsetA(instance=inventory, form_kwargs={'user': request.user})
        formset_b = forms.TTProductToInventoryFormsetB(instance=product_batch, form_kwargs={'user': request.user})
        
        if form.is_valid():
            total_amount = form.cleaned_data['total_amount'] 
            total_quantity = form.cleaned_data['total_quantity']
            product_batch = form.cleaned_data['product_batch']
            inventory = form.cleaned_data['inventory']
            
            form = forms.TTProductToInventoryForm(request.POST, instance=user, user=user)
            formset_a = forms.TTProductToInventoryFormsetA(instance=inventory, form_kwargs={'user': request.user})
            formset_b = forms.TTProductToInventoryFormsetB(instance=product_batch, form_kwargs={'user': request.user})

            # Create a new Product instance and associate it with the inventory
            inventory_batch = TT_Inventory_Product.objects.create(user=request.user,inventory=inventory, product_batch=product_batch, total_amount=total_amount, remaining_amount=total_amount, total_quantity=total_quantity, remaining_quantity=total_quantity)

            # Update the product batch amount (weight) and quantity
            product_batch.remaining_weight -= total_amount
            product_batch.remaining_quantity -= total_quantity
            product_batch.save()
            form.save()
            
            return redirect('home')
    
    else:
        inventory = None
        product_batch = None
        user = request.user
        
        form = forms.TTProductToInventoryForm(user=user)
        formset_a = forms.TTProductToInventoryFormsetA(instance=inventory, form_kwargs={'user': request.user})
        formset_b = forms.TTProductToInventoryFormsetB(instance=product_batch, form_kwargs={'user': request.user})

    return render(request, 'tracker/tt_product_to_inventory_form.html', {'form': form})

@login_required
def inventory_to_stop_item(request):
    
    if request.method == 'POST':

        inventory_product = None
        user = request.user

        form = forms.TTInventoryToStopItemForm(request.POST)
        formset_a = forms.TTInventoryToStopItemFormsetA(instance=inventory_product, form_kwargs={'user': request.user})

        if form.is_valid():
            weight = form.cleaned_data['weight'] 
            quantity = form.cleaned_data['quantity']
            inventory_product = form.cleaned_data['inventory_product']
            
            form = forms.TTInventoryToStopItemForm(request.POST, instance=user, user=user)
            formset_a = forms.TInventoryToStopItemFormsetA(instance=inventory_product, form_kwargs={'user': request.user})


            # Create a new Stop Item instance and associate it with the inventory
            stop_item = Stop_Item.objects.create(user=request.user,inventory_product=inventory_product, weight=weight, quantity=quantity, quantity_received=quantity)

            # Update the product batch amount (weight) and quantity
            inventory_product.remaining_weight -= weight
            inventory_product.remaining_quantity -= quantity
            inventory_product.save()
            form.save()
            
            return redirect('home')
    
    else:
        inventory_product = None
        user = request.user
        
        form = forms.TTInventoryToStopItemForm(user=user)
        formset_a = forms.TTInventoryToStopItemFormsetA(instance=inventory_product, form_kwargs={'user': request.user})

    return render(request, 'tracker/tt_inventory_to_stop_item_form.html', {'form': form})

@login_required
def inventory_to_invoice_item(request):
    
    if request.method == 'POST':

        invoice_model = None
        inventory_product = None
        user = request.user
        
        form = forms.TTInventoryToInvoiceItemForm(request.POST,user=user)
        formset_a = forms.TTInventoryToInvoiceItemFormsetA(instance=invoice_model, form_kwargs={'user': request.user})
        formset_b = forms.TTInventoryToInvoiceItemFormsetB(instance=inventory_product, form_kwargs={'user': request.user})
        
        if form.is_valid():
            quantity = form.cleaned_data['amount']
            invoice_model = form.cleaned_date['invoice_model']
            inventory_product = form.cleaned_data['inventory_product']
            
            
            form = forms.TTInventoryToInvoiceItemForm(request.POST, instance=user, user=user)
            formset_a = forms.TTInventoryToInvoiceItemFormsetA(instance=invoice_model, form_kwargs={'user': request.user})
            formset_b = forms.TTInventoryToInvoiceItemFormsetB(instance=inventory_product, form_kwargs={'user': request.user})

            # Create a new Stop Item instance and associate it with the inventory
            invoice_item = Invoice_Inventory.objects.create(user=request.user,inventory_product=inventory_product,invoice_model=invoice_model, amount=quantity)

            # Update the product batch amount (weight) and quantity
            inventory_product.remaining_quantity -= quantity
            inventory_product.save()
            form.save()
            
            return redirect('home')
    
    else:
        invoice_model = None
        inventory_product = None
        user = request.user
        
        form = forms.TTInventoryToInvoiceItemForm(user=user)
        formset_a = forms.TTInventoryToInvoiceItemFormsetA(instance=invoice_model, form_kwargs={'user': request.user})
        formset_b = forms.TTInventoryToInvoiceItemFormsetB(instance=inventory_product, form_kwargs={'user': request.user})

    return render(request, 'tracker/tt_inventory_to_stop_item_form.html', {'form': form})


# Custom User-Only Model Create Views
# ===================================
@login_required
def strain_create_form(request):
    
    if request.method == 'POST':

        user = request.user

        form = forms.StrainCreateForm(request.POST,user=user)
        
        if form.is_valid():
            
            # Gather cleaned input data from fields
            # Example: quantity = form.cleaned_data['amount']
            name = form.cleaned_data['name']

            form = forms.StrainCreateForm(request.POST, instance=user, user=user)
        
            
            # Create a new Model instance and associate it with the batch
            strain = Strain.objects.create(user=request.user, name=name)

            # Make additional manipulations
            # Example: inventory_product.remaining_quantity -= quantity
            
            # Save
            form.save()
            
            return redirect('home')
    
    else:
        user = request.user
        form = forms.StrainCreateForm(user=user)

    return render(request, 'tracker/strain_create_form.html', {'form': form})

@login_required
def lab_result_create_form(request):
    
    if request.method == 'POST':

        user = request.user

        form = forms.LabResultCreateForm(request.POST,user=user)
        
        if form.is_valid():
            
            # Gather cleaned input data from fields
            # Example: quantity = form.cleaned_data['amount']
            name = form.cleaned_data['name']

            form = forms.LabResultCreateForm(request.POST, instance=user, user=user)
        
            # Create a new Model instance and associate it with the batch
            lab_result = Lab_Result.objects.create(user=request.user, name=name)

            # Make additional manipulations
            # Example: inventory_product.remaining_quantity -= quantity
            
            # Save
            form.save()
            
            return redirect('home')
    
    else:
        user = request.user
        form = forms.LabResultCreateForm(user=user)

    return render(request, 'tracker/lab_result_create_form.html', {'form': form})

@login_required
def lab_sample_result_create_form(request):
    
    if request.method == 'POST':

        user = request.user

        form = forms.LabSampleResultCreateForm(request.POST,user=user)
        
        if form.is_valid():
            
            # Gather cleaned input data from fields
            # Example: quantity = form.cleaned_data['amount']
            sample_name = form.cleaned_data['sample_name']

            form = forms.LabSampleResultCreateForm(request.POST, instance=user, user=user)
        
            # Create a new Model instance and associate it with the batch
            lab_sample_result = Lab_Sample_Result.objects.create(user=request.user, sample_name=sample_name)

            # Make additional manipulations
            # Example: inventory_product.remaining_quantity -= quantity
            
            # Save
            form.save()
            
            return redirect('home')
    
    else:
        user = request.user
        form = forms.LabSampleResultCreateForm(user=user)

    return render(request, 'tracker/lab_sample_result_create_form.html', {'form': form})


@login_required
def tt_user_info_create_form(request):
    
    if request.method == 'POST':

        user = request.user

        form = forms.TTUserInfoCreateForm(request.POST,user=user)
        
        if form.is_valid():
            
            # Gather cleaned input data from fields
            # Example: quantity = form.cleaned_data['amount']
            company_name = form.cleaned_data['company_name']

            form = forms.TTUserInfoCreateForm(request.POST, instance=user, user=user)
        
            # Create a new Model instance and associate it with the batch
            user_info = TT_User_Info.objects.create(user=request.user, company_name=company_name)

            # Make additional manipulations
            # Example: inventory_product.remaining_quantity -= quantity
            
            # Save
            form.save()
            
            return redirect('home')
    
    else:
        user = request.user
        form = forms.TTUserInfoCreateForm(user=user)

    return render(request, 'tracker/tt_user_info_create_form.html', {'form': form})



@login_required
def tt_location_create_form(request):
    
    if request.method == 'POST':

        user = request.user

        form = forms.TTLocationCreateForm(request.POST,user=user)
        
        if form.is_valid():
            
            # Gather cleaned input data from fields
            # Example: quantity = form.cleaned_data['amount']
            name = form.cleaned_data['name']

            form = forms.TTLocationCreateForm(request.POST, instance=user, user=user)
        
            # Create a new Model instance and associate it with the batch
            location = TT_Location.objects.create(user=request.user, name=name)

            # Make additional manipulations
            # Example: inventory_product.remaining_quantity -= quantity
            
            # Save
            form.save()
            
            return redirect('home')
    
    else:
        user = request.user
        form = forms.TTLocationCreateForm(user=user)

    return render(request, 'tracker/tt_location_create_form.html', {'form': form})

@login_required
def tt_sublot_create_form(request):
    
    if request.method == 'POST':

        location = None
        user = request.user

        form = forms.TTSublotCreateForm(request.POST,user=user)
        formset = forms.TTSublotCreateFormset(instance=location, form_kwargs={'user': request.user})
        
        if form.is_valid():
            
            # Gather cleaned input data from fields
            # Example: quantity = form.cleaned_data['amount']
            location = form.cleaned_data['location']
            sublot_name = form.cleaned_data['sublot_name']

            form = forms.TTSublotCreateForm(request.POST, instance=location, user=user)
            formset = forms.TTSublotCreateFormset(request.POST, instance=location, form_kwargs={'user': request.user})
            
            # Create a new Model instance and associate it with the batch
            sublot = TT_Sublot.objects.create(user=request.user, location=location, sublot_name=sublot_name)

            # Make additional manipulations
            # Example: inventory_product.remaining_quantity -= quantity
            
            # Save
            form.save()
            
            return redirect('home')
    
    else:

        location = None
        user = request.user

        #form = forms.TTPlantBatchHarvestCreateForm

        form = forms.TTSublotCreateForm(user=user)
        formset = forms.TTSublotCreateFormset(instance=location, form_kwargs={'user': request.user})

    return render(request, 'tracker/tt_sublot_create_form.html', {'form': form})

@login_required
def tt_plant_batch_create_form(request):
    
    if request.method == 'POST':

        strain = None
        location = None
        sublot = None
        user = request.user

        form = forms.TTPlantBatchCreateForm(request.POST,user=user)
        formset_a = forms.TTPlantBatchCreateFormsetA(instance=strain, form_kwargs={'user': request.user})
        formset_b = forms.TTPlantBatchCreateFormsetB(instance=location, form_kwargs={'user': request.user})
        formset_c = forms.TTPlantBatchCreateFormsetC(instance=sublot, form_kwargs={'user': request.user})

        
        if form.is_valid():
            
            # Gather cleaned input data from fields
            # Example: quantity = form.cleaned_data['amount']
            strain = form.cleaned_data['strain']
            location = form.cleaned_data['location']
            sublot = form.cleaned_data['sublot']
            
            form = forms.TTPlantBatchCreateForm(request.POST, instance=location, user=user)
            formset_a = forms.TTPlantBatchCreateFormsetA(instance=strain, form_kwargs={'user': request.user})
            formset_b = forms.TTPlantBatchCreateFormsetB(instance=location, form_kwargs={'user': request.user})
            formset_c = forms.TTPlantBatchCreateFormsetC(instance=sublot, form_kwargs={'user': request.user})
            
            # Create a new Model instance and associate it with the batch
            plant_batch = TT_Plant_Batch.objects.create(user=request.user, strain=strain, location=location, sublot=sublot)

            # Make additional manipulations
            # Example: inventory_product.remaining_quantity -= quantity
            
            # Save
            form.save()
            
            return redirect('home')
    
    else:

        strain = None
        location = None
        sublot = None
        user = request.user

        #form = forms.TTPlantBatchHarvestCreateForm

        form = forms.TTPlantBatchCreateForm(user=user)
        formset_a = forms.TTPlantBatchCreateFormsetA(instance=strain, form_kwargs={'user': request.user})
        formset_b = forms.TTPlantBatchCreateFormsetB(instance=location, form_kwargs={'user': request.user})
        formset_c = forms.TTPlantBatchCreateFormsetC(instance=sublot, form_kwargs={'user': request.user})

    return render(request, 'tracker/tt_plant_batch_create_form.html', {'form': form})


@login_required
def tt_plant_batch_harvest_create_form(request):
    
    if request.method == 'POST':

        plant_batch = None
        location = None
        sublot = None
        user = request.user

        form = forms.TTPlantBatchHarvestCreateForm(request.POST,user=user)
        formset_a = forms.TTPlantBatchHarvestCreateFormsetA(instance=plant_batch, form_kwargs={'user': request.user})
        formset_b = forms.TTPlantBatchHarvestCreateFormsetB(instance=location, form_kwargs={'user': request.user})
        formset_c = forms.TTPlantBatchHarvestCreateFormsetC(instance=sublot, form_kwargs={'user': request.user})
        
        if form.is_valid():
            
            # Gather cleaned input data from fields
            # Example: quantity = form.cleaned_data['amount']
            plant_batch = form.cleaned_data['plant_batch']
            location = form.cleaned_data['location']
            sublot = form.cleaned_data['sublot']
            total_dry_weight = form.cleaned_data['total_dry_weight']
            total_wet_weight = form.cleaned_data['total_wet_weight']

            form = forms.TTPlantBatchHarvestCreateForm(request.POST, instance=plant_batch, user=user)
            formset_a = forms.TTPlantBatchHarvestCreateFormsetA(instance=plant_batch, form_kwargs={'user': request.user})
            formset_b = forms.TTPlantBatchHarvestCreateFormsetB(instance=location, form_kwargs={'user': request.user})
            formset_c = forms.TTPlantBatchHarvestCreateFormsetC(instance=sublot, form_kwargs={'user': request.user})
            
            # Create a new Model instance and associate it with the batch
            harvest_batch = TT_Plant_Batch_Harvest.objects.create(user=request.user, plant_batch=plant_batch, location=location, sublot=sublot, total_wet_weight=total_wet_weight,total_dry_weight=total_dry_weight,remaining_wet_weight=total_wet_weight, remaining_dry_weight=total_dry_weight)

            # Make additional manipulations
            # Example: inventory_product.remaining_quantity -= quantity
            
            # Save
            form.save()
            
            return redirect('home')
    
    else:

        plant_batch = None
        location = None
        sublot = None
        user = request.user

        #form = forms.TTPlantBatchHarvestCreateForm

        form = forms.TTPlantBatchHarvestCreateForm(user=user)
        formset_a = forms.TTPlantBatchHarvestCreateFormsetA(instance=plant_batch, form_kwargs={'user': request.user})
        formset_b = forms.TTPlantBatchHarvestCreateFormsetB(instance=location, form_kwargs={'user': request.user})
        formset_c = forms.TTPlantBatchHarvestCreateFormsetC(instance=sublot, form_kwargs={'user': request.user})

    return render(request, 'tracker/tt_plant_batch_harvest_create_form.html', {'form': form})

@login_required
def tt_inventory_create_form(request):
    
    if request.method == 'POST':

        location = None
        sublot = None
        user = request.user

        form = forms.TTInventoryCreateForm(request.POST,user=user)
        formset_a = forms.TTInventoryCreateFormsetA(instance=location, form_kwargs={'user': request.user})
        formset_b = forms.TTInventoryCreateFormsetB(instance=sublot, form_kwargs={'user': request.user})
        
        if form.is_valid():
            
            # Gather cleaned input data from fields
            # Example: quantity = form.cleaned_data['amount']
            location = form.cleaned_data['location']
            sublot = form.cleaned_data['sublot']
            inventory_name = form.cleaned_data['inventory_name']

            form = forms.TTInventoryCreateForm(request.POST, instance=user, user=user)
            formset_a = forms.TTInventoryCreateFormsetA(instance=location, form_kwargs={'user': request.user})
            formset_b = forms.TTInventoryCreateFormsetB(instance=sublot, form_kwargs={'user': request.user})
            
            # Create a new Model instance and associate it with the batch
            inventory = TT_Inventory.objects.create(user=request.user, inventory_name=inventory_name, location=location, sublot=sublot)

            # Make additional manipulations
            # Example: inventory_product.remaining_quantity -= quantity
            
            # Save
            form.save()
            
            return redirect('home')
    
    else:

        location = None
        sublot = None
        user = request.user

        form = forms.TTInventoryCreateForm(user=user)
        formset_a = forms.TTInventoryCreateFormsetA(instance=location, form_kwargs={'user': request.user})
        formset_b = forms.TTInventoryCreateFormsetB(instance=sublot, form_kwargs={'user': request.user})

    return render(request, 'tracker/tt_inventory_create_form.html', {'form': form})

@login_required
def invoice_model_create_form(request):
    
    if request.method == 'POST':

        inventory = None
        user = request.user

        form = forms.InvoiceModelCreateForm(request.POST,user=user)
        formset_a = forms.InvoiceModelCreateFormsetA(instance=inventory, form_kwargs={'user': request.user})
        
        if form.is_valid():
            
            # Gather cleaned input data from fields
            # Example: quantity = form.cleaned_data['amount']
            inventory = form.cleaned_data['inventory']
            invoice_name = form.cleaned_data['invoice_name']

            form = forms.InvoiceModelCreateForm(request.POST, instance=user, user=user)
            formset_a = forms.InvoiceModelCreateFormsetA(instance=inventory, form_kwargs={'user': request.user})
            
            # Create a new Model instance and associate it with the batch
            invoice = Invoice_Model.objects.create(user=request.user, invoice_name=invoice_name, inventory=inventory)

            # Make additional manipulations
            # Example: inventory_product.remaining_quantity -= quantity
            
            # Save
            form.save()
            
            return redirect('home')
    
    else:

        inventory = None
        user = request.user

        form = forms.InvoiceModelCreateForm(user=user)
        formset_a = forms.InvoiceModelCreateFormsetA(instance=inventory, form_kwargs={'user': request.user})

    return render(request, 'tracker/invoice_model_create_form.html', {'form': form})




# Toggle Delete Views
# ===================
@login_required
def tt_location_delete_form(request):
    
    if request.method == 'POST':

        deleted_item = None
        user = request.user

        form = forms.TTLocationDeleteForm(request.POST,user=user)
        formset_a = forms.TTLocationDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


        if form.is_valid():

            deleted_item = form.cleaned_data['deleted_item'] 

            form = forms.TTLocationDeleteForm(request.POST, instance=user, user=user)
            formset_a = forms.TTLocationDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


            # Create a new Product instance and associate it with the inventory
            delete_batch = TT_Location_Delete.objects.create(user=request.user,deleted_item=deleted_item)

            # Update the product batch amount (weight) and quantity
            deleted_item.deleted = True
            deleted_item.save()
            form.save()
            
            return redirect('home')
    else:
        
        deleted_item = None
        user = request.user

        form = forms.TTLocationDeleteForm(user=user)
        formset_a = forms.TTLocationDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})

    return render(request, 'tracker/tt_location_delete_form.html', {'form': form})


@login_required
def tt_sublot_delete_form(request):
    
    if request.method == 'POST':

        deleted_item = None
        user = request.user

        form = forms.TTSublotDeleteForm(request.POST,user=user)
        formset_a = forms.TTSublotDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


        if form.is_valid():

            deleted_item = form.cleaned_data['deleted_item'] 

            form = forms.TTSublotDeleteForm(request.POST, instance=user, user=user)
            formset_a = forms.TTSublotDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


            # Create a new Product instance and associate it with the inventory
            delete_batch = TT_Sublot_Delete.objects.create(user=request.user,deleted_item=deleted_item)

            # Update the product batch amount (weight) and quantity
            deleted_item.deleted = True
            deleted_item.save()
            form.save()
            
            return redirect('home')
    else:
        
        deleted_item = None
        user = request.user

        form = forms.TTSublotDeleteForm(user=user)
        formset_a = forms.TTSublotDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})

    return render(request, 'tracker/tt_sublot_delete_form.html', {'form': form})


@login_required
def strain_delete_form(request):
    
    if request.method == 'POST':

        deleted_item = None
        user = request.user

        form = forms.StrainDeleteForm(request.POST,user=user)
        formset_a = forms.StrainDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


        if form.is_valid():

            deleted_item = form.cleaned_data['deleted_item'] 

            form = forms.StrainDeleteForm(request.POST, instance=user, user=user)
            formset_a = forms.StrainDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


            # Create a new Product instance and associate it with the inventory
            delete_batch = Strain_Delete.objects.create(user=request.user,deleted_item=deleted_item)

            # Update the product batch amount (weight) and quantity
            deleted_item.deleted = True
            deleted_item.save()
            form.save()
            
            return redirect('home')
    else:
        
        deleted_item = None
        user = request.user

        form = forms.StrainDeleteForm(user=user)
        formset_a = forms.StrainDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})

    return render(request, 'tracker/strain_delete_form.html', {'form': form})


@login_required
def tt_plant_batch_delete_form(request):
    
    if request.method == 'POST':

        deleted_item = None
        user = request.user

        form = forms.TTPlantBatchDeleteForm(request.POST,user=user)
        formset_a = forms.TTPlantBatchDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


        if form.is_valid():

            deleted_item = form.cleaned_data['deleted_item'] 

            form = forms.TTPlantBatchDeleteForm(request.POST, instance=user, user=user)
            formset_a = forms.TTPlantBatchDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


            # Create a new Product instance and associate it with the inventory
            delete_batch = TT_Plant_Batch_Delete.objects.create(user=request.user,deleted_item=deleted_item)

            # Update the product batch amount (weight) and quantity
            deleted_item.deleted = True
            deleted_item.save()
            form.save()
            
            return redirect('home')
    else:
        
        deleted_item = None
        user = request.user

        form = forms.TTPlantBatchDeleteForm(user=user)
        formset_a = forms.TTPlantBatchDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})

    return render(request, 'tracker/tt_plant_batch_delete_form.html', {'form': form})


@login_required
def tt_plant_batch_harvest_delete_form(request):
    
    if request.method == 'POST':

        deleted_item = None
        user = request.user

        form = forms.TTPlantBatchHarvestDeleteForm(request.POST,user=user)
        formset_a = forms.TTPlantBatchHarvestDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


        if form.is_valid():

            deleted_item = form.cleaned_data['deleted_item'] 

            form = forms.TTPlantBatchHarvestDeleteForm(request.POST, instance=user, user=user)
            formset_a = forms.TTPlantBatchHarvestDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


            # Create a new Product instance and associate it with the inventory
            delete_batch = TT_Plant_Batch_Harvest_Delete.objects.create(user=request.user,deleted_item=deleted_item)

            # Update the product batch amount (weight) and quantity
            deleted_item.deleted = True
            deleted_item.save()
            form.save()
            
            return redirect('home')
    else:
        
        deleted_item = None
        user = request.user

        form = forms.TTPlantBatchHarvestDeleteForm(user=user)
        formset_a = forms.TTPlantBatchHarvestDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})

    return render(request, 'tracker/tt_plant_batch_harvest_delete_form.html', {'form': form})

@login_required
def tt_storage_batch_delete_form(request):
    
    if request.method == 'POST':

        deleted_item = None
        user = request.user

        form = forms.TTStorageBatchDeleteForm(request.POST,user=user)
        formset_a = forms.TTStorageBatchDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


        if form.is_valid():

            deleted_item = form.cleaned_data['deleted_item'] 

            form = forms.TTStorageBatchDeleteForm(request.POST, instance=user, user=user)
            formset_a = forms.TTStorageBatchDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


            # Create a new Product instance and associate it with the inventory
            delete_batch = TT_Storage_Batch_Delete.objects.create(user=request.user,deleted_item=deleted_item)

            # Update the product batch amount (weight) and quantity
            deleted_item.deleted = True
            deleted_item.save()
            form.save()
            
            return redirect('home')
    else:
        
        deleted_item = None
        user = request.user

        form = forms.TTStorageBatchDeleteForm(user=user)
        formset_a = forms.TTStorageBatchDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})

    return render(request, 'tracker/tt_storage_batch_delete_form.html', {'form': form})


@login_required
def tt_product_batch_delete_form(request):
    
    if request.method == 'POST':

        deleted_item = None
        user = request.user

        form = forms.TTProductBatchDeleteForm(request.POST,user=user)
        formset_a = forms.TTProductBatchDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


        if form.is_valid():

            deleted_item = form.cleaned_data['deleted_item'] 

            form = forms.TTProductBatchDeleteForm(request.POST, instance=user, user=user)
            formset_a = forms.TTProductBatchDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


            # Create a new Product instance and associate it with the inventory
            delete_batch = TT_Product_Batch_Delete.objects.create(user=request.user,deleted_item=deleted_item)

            # Update the product batch amount (weight) and quantity
            deleted_item.deleted = True
            deleted_item.save()
            form.save()
            
            return redirect('home')
    else:
        
        deleted_item = None
        user = request.user

        form = forms.TTProductBatchDeleteForm(user=user)
        formset_a = forms.TTProductBatchDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})

    return render(request, 'tracker/tt_product_batch_delete_form.html', {'form': form})


@login_required
def lab_result_delete_form(request):
    
    if request.method == 'POST':

        deleted_item = None
        user = request.user

        form = forms.LabResultDeleteForm(request.POST,user=user)
        formset_a = forms.LabResultDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


        if form.is_valid():

            deleted_item = form.cleaned_data['deleted_item'] 

            form = forms.LabResultDeleteForm(request.POST, instance=user, user=user)
            formset_a = forms.LabResultDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


            # Create a new Product instance and associate it with the inventory
            delete_batch = Lab_Result_Delete.objects.create(user=request.user,deleted_item=deleted_item)

            # Update the product batch amount (weight) and quantity
            deleted_item.deleted = True
            deleted_item.save()
            form.save()
            
            return redirect('home')
    else:
        
        deleted_item = None
        user = request.user

        form = forms.LabResultDeleteForm(user=user)
        formset_a = forms.LabResultDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})

    return render(request, 'tracker/lab_result_delete_form.html', {'form': form})


@login_required
def lab_sample_result_delete_form(request):
    
    if request.method == 'POST':

        deleted_item = None
        user = request.user

        form = forms.LabSampleResultDeleteForm(request.POST,user=user)
        formset_a = forms.LabSampleResultDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


        if form.is_valid():

            deleted_item = form.cleaned_data['deleted_item'] 

            form = forms.LabSampleResultDeleteForm(request.POST, instance=user, user=user)
            formset_a = forms.LabSampleResultDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


            # Create a new Product instance and associate it with the inventory
            delete_batch = Lab_Sample_Result_Delete.objects.create(user=request.user,deleted_item=deleted_item)

            # Update the product batch amount (weight) and quantity
            deleted_item.deleted = True
            deleted_item.save()
            form.save()
            
            return redirect('home')
    else:
        
        deleted_item = None
        user = request.user

        form = forms.LabSampleResultDeleteForm(user=user)
        formset_a = forms.LabSampleResultDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})

    return render(request, 'tracker/lab_sample_result_delete_form.html', {'form': form})


@login_required
def tt_lab_sample_delete_form(request):
    
    if request.method == 'POST':

        deleted_item = None
        user = request.user

        form = forms.TTLabSampleDeleteForm(request.POST,user=user)
        formset_a = forms.TTLabSampleDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


        if form.is_valid():

            deleted_item = form.cleaned_data['deleted_item'] 

            form = forms.TTLabSampleDeleteForm(request.POST, instance=user, user=user)
            formset_a = forms.TTLabSampleDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


            # Create a new Product instance and associate it with the inventory
            delete_batch = TT_Lab_Sample_Delete.objects.create(user=request.user,deleted_item=deleted_item)

            # Update the product batch amount (weight) and quantity
            deleted_item.deleted = True
            deleted_item.save()
            form.save()
            
            return redirect('home')
    else:
        
        deleted_item = None
        user = request.user

        form = forms.TTLabSampleDeleteForm(user=user)
        formset_a = forms.TTLabSampleDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})

    return render(request, 'tracker/tt_lab_sample_delete_form.html', {'form': form})


@login_required
def tt_inventory_delete_form(request):
    
    if request.method == 'POST':

        deleted_item = None
        user = request.user

        form = forms.TTInventoryDeleteForm(request.POST,user=user)
        formset_a = forms.TTInventoryDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


        if form.is_valid():

            deleted_item = form.cleaned_data['deleted_item'] 

            form = forms.TTInventoryDeleteForm(request.POST, instance=user, user=user)
            formset_a = forms.TTInventoryDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


            # Create a new Product instance and associate it with the inventory
            delete_batch = TT_Inventory_Delete.objects.create(user=request.user,deleted_item=deleted_item)

            # Update the product batch amount (weight) and quantity
            deleted_item.deleted = True
            deleted_item.save()
            form.save()
            
            return redirect('home')
    else:
        
        deleted_item = None
        user = request.user

        form = forms.TTInventoryDeleteForm(user=user)
        formset_a = forms.TTInventoryDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})

    return render(request, 'tracker/tt_inventory_delete_form.html', {'form': form})

@login_required
def tt_inventory_product_delete_form(request):
    
    if request.method == 'POST':

        deleted_item = None
        user = request.user

        form = forms.TTInventoryProductDeleteForm(request.POST,user=user)
        formset_a = forms.TTInventoryProductDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


        if form.is_valid():

            deleted_item = form.cleaned_data['deleted_item'] 

            form = forms.TTInventoryProductDeleteForm(request.POST, instance=user, user=user)
            formset_a = forms.TTInventoryProductDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


            # Create a new Product instance and associate it with the inventory
            delete_batch = TT_Inventory_Product_Delete.objects.create(user=request.user,deleted_item=deleted_item)

            # Update the product batch amount (weight) and quantity
            deleted_item.deleted = True
            deleted_item.save()
            form.save()
            
            return redirect('home')
    else:
        
        deleted_item = None
        user = request.user

        form = forms.TTInventoryProductDeleteForm(user=user)
        formset_a = forms.TTInventoryProductDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})

    return render(request, 'tracker/tt_inventory_product_delete_form.html', {'form': form})


@login_required
def invoice_model_delete_form(request):
    
    if request.method == 'POST':

        deleted_item = None
        user = request.user

        form = forms.InvoiceModelDeleteForm(request.POST,user=user)
        formset_a = forms.InvoiceModelDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


        if form.is_valid():

            deleted_item = form.cleaned_data['deleted_item'] 

            form = forms.InvoiceModelDeleteForm(request.POST, instance=user, user=user)
            formset_a = forms.InvoiceModelDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


            # Create a new Product instance and associate it with the inventory
            delete_batch = Invoice_Model_Delete.objects.create(user=request.user,deleted_item=deleted_item)

            # Update the product batch amount (weight) and quantity
            deleted_item.deleted = True
            deleted_item.save()
            form.save()
            
            return redirect('home')
    else:
        
        deleted_item = None
        user = request.user

        form = forms.InvoiceModelDeleteForm(user=user)
        formset_a = forms.InvoiceModelDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})

    return render(request, 'tracker/invoice_model_delete_form.html', {'form': form})


@login_required
def invoice_inventory_delete_form(request):
    
    if request.method == 'POST':

        deleted_item = None
        user = request.user

        form = forms.InvoiceInventoryDeleteForm(request.POST,user=user)
        formset_a = forms.InvoiceInventoryDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


        if form.is_valid():

            deleted_item = form.cleaned_data['deleted_item'] 

            form = forms.InvoiceInventoryDeleteForm(request.POST, instance=user, user=user)
            formset_a = forms.InvoiceInventoryDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})


            # Create a new Product instance and associate it with the inventory
            delete_batch = Invoice_Inventory_Delete.objects.create(user=request.user,deleted_item=deleted_item)

            # Update the product batch amount (weight) and quantity
            deleted_item.deleted = True
            deleted_item.save()
            form.save()
            
            return redirect('home')
    else:
        
        deleted_item = None
        user = request.user

        form = forms.InvoiceInventoryDeleteForm(user=user)
        formset_a = forms.InvoiceInventoryDeleteFormsetA(instance=deleted_item, form_kwargs={'user': request.user})

    return render(request, 'tracker/invoice_inventory_delete_form.html', {'form': form})




# Filter & Search Views
# =====================

class TTPlantBatchHarvestSearch(LoginRequiredMixin, View):
    template_name = 'tracker/tt_plant_batch_harvest_search.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')

        if query:
            results = TT_Plant_Batch_Harvest.objects.filter(plant_batch__strain__name__icontains=query)
            # change the filter to a char field input
        else:
            results = TT_Plant_Batch_Harvest.objects.all()

        context = {'results': results, 'query': query}
        return render(request, self.template_name, context)



# Create Update Delete Template Views
# ===================================

class StrainCreate(LoginRequiredMixin,CreateView):
    model = Strain
    fields = '__all__'

class StrainUpdate(LoginRequiredMixin,UpdateView):
    model = Strain
    fields = '__all__'
    success_url = reverse_lazy('home')

class StrainDelete(LoginRequiredMixin,DeleteView):
    model = Strain
    success_url = reverse_lazy('home')

class TTInventoryCreate(LoginRequiredMixin,CreateView):
    model = TT_Inventory
    fields = '__all__'

class TTInventoryUpdate(LoginRequiredMixin,UpdateView):
    model = TT_Inventory
    fields = '__all__'
    success_url = reverse_lazy('home')

class TTInventoryDelete(LoginRequiredMixin,DeleteView):
    model = TT_Inventory
    success_url = reverse_lazy('home')

class TTInventoryProductCreate(LoginRequiredMixin,CreateView):
    model = TT_Inventory_Product
    fields = '__all__'

class TTInventoryProductUpdate(LoginRequiredMixin,UpdateView):
    model = TT_Inventory_Product
    fields = '__all__'
    success_url = reverse_lazy('home')

class TTInventoryProductDelete(LoginRequiredMixin,DeleteView):
    model = TT_Inventory_Product
    success_url = reverse_lazy('home')

class TTUserInfoCreate(LoginRequiredMixin,CreateView):
    model = TT_User_Info
    fields = '__all__'

class TTUserInfoUpdate(LoginRequiredMixin,UpdateView):
    model = TT_User_Info
    fields = '__all__'
    success_url = reverse_lazy('home')

class TTUserInfoDelete(LoginRequiredMixin,DeleteView):
    model = TT_User_Info
    success_url = reverse_lazy('home')

class TTLocationCreate(LoginRequiredMixin,CreateView):
    model = TT_Location
    fields = '__all__'

class TTLocationUpdate(LoginRequiredMixin,UpdateView):
    model = TT_Location
    fields = '__all__'
    success_url = reverse_lazy('home')

class TTLocationDelete(LoginRequiredMixin,DeleteView):
    model = TT_Location
    success_url = reverse_lazy('home')

class TTPlantBatchCreate(LoginRequiredMixin,CreateView):
    model = TT_Plant_Batch
    fields = '__all__'

class TTPlantBatchUpdate(LoginRequiredMixin,UpdateView):
    model = TT_Plant_Batch
    fields = '__all__'
    success_url = reverse_lazy('home')

class TTPlantBatchDelete(LoginRequiredMixin,DeleteView):
    model = TT_Plant_Batch
    success_url = reverse_lazy('home')

class TTPlantBatchHarvestCreate(LoginRequiredMixin,CreateView):
    model = TT_Plant_Batch_Harvest
    fields = ['deleted','plant_batch','location','sublot','from_row','to_row','harvest_stage','harvest_completed','harvest_start_date','harvest_finish_date','external_id','harvest_id','biotrack_id','transaction_id','total_wet_weight','total_dry_weight','remaining_wet_weight','remaining_dry_weight','notes']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TTPlantBatchHarvestUpdate(LoginRequiredMixin,UpdateView):
    model = TT_Plant_Batch_Harvest
    fields = ['deleted','plant_batch','location','sublot','from_row','to_row','harvest_stage','harvest_completed','harvest_start_date','harvest_finish_date','external_id','harvest_id','biotrack_id','transaction_id','total_wet_weight','total_dry_weight','remaining_wet_weight','remaining_dry_weight','notes']
    success_url = reverse_lazy('home')

    def get_queryset(self):
        user = self.request.user
        return TT_Plant_Batch_Harvest.objects.filter(user=user)

class TTPlantBatchHarvestDelete(LoginRequiredMixin,DeleteView):
    model = TT_Plant_Batch_Harvest
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return TT_Plant_Batch_Harvest.objects.filter(user=self.request.user)

class TTStorageBatchCreate(LoginRequiredMixin,CreateView):
    model = TT_Storage_Batch
    fields = '__all__'

class TTStorageBatchUpdate(LoginRequiredMixin,UpdateView):
    model = TT_Storage_Batch
    fields = '__all__'
    success_url = reverse_lazy('home')

class TTStorageBatchDelete(LoginRequiredMixin,DeleteView):
    model = TT_Storage_Batch
    success_url = reverse_lazy('home')

class TTProductBatchCreate(LoginRequiredMixin,CreateView):
    model = TT_Product_Batch
    fields = '__all__'

class TTProductBatchUpdate(LoginRequiredMixin,UpdateView):
    model = TT_Product_Batch
    fields = '__all__'
    success_url = reverse_lazy('home')

class TTProductBatchDelete(LoginRequiredMixin,DeleteView):
    model = TT_Product_Batch
    success_url = reverse_lazy('home')

class TTSublotCreate(LoginRequiredMixin,CreateView):
    model = TT_Sublot
    fields = '__all__'

class TTSublotUpdate(LoginRequiredMixin,UpdateView):
    model = TT_Sublot
    fields = '__all__'
    success_url = reverse_lazy('home')

class TTSublotDelete(LoginRequiredMixin,DeleteView):
    model = TT_Sublot
    success_url = reverse_lazy('home')

class TTLabSampleCreate(LoginRequiredMixin,CreateView):
    model = TT_Lab_Sample
    fields = '__all__'

class TTLabSampleUpdate(LoginRequiredMixin,UpdateView):
    model = TT_Lab_Sample
    fields = '__all__'
    success_url = reverse_lazy('home')

class TTLabSampleDelete(LoginRequiredMixin,DeleteView):
    model = TT_Lab_Sample
    success_url = reverse_lazy('home')

class PlantCreate(LoginRequiredMixin,CreateView):
    model = Plant
    fields = '__all__'

class PlantUpdate(LoginRequiredMixin,UpdateView):
    model = Plant
    fields = '__all__'
    success_url = reverse_lazy('home')

class PlantDelete(LoginRequiredMixin,DeleteView):
    model = Plant
    success_url = reverse_lazy('home')

class WeightCreate(LoginRequiredMixin,CreateView):
    model = Weight
    fields = '__all__'

class WeightUpdate(LoginRequiredMixin,UpdateView):
    model = Weight
    fields = '__all__'
    success_url = reverse_lazy('home')

class WeightDelete(LoginRequiredMixin,DeleteView):
    model = Weight
    success_url = reverse_lazy('home')

class DerivativeCreate(LoginRequiredMixin,CreateView):
    model = Derivative
    fields = '__all__'

class DerivativeUpdate(LoginRequiredMixin,UpdateView):
    model = Derivative
    fields = '__all__'
    success_url = reverse_lazy('home')

class DerivativeDelete(LoginRequiredMixin,DeleteView):
    model = Derivative
    success_url = reverse_lazy('home')

class PlantHarvestCreate(LoginRequiredMixin,CreateView):
    model = Plant_Harvest
    fields = '__all__'

class PlantHarvestUpdate(LoginRequiredMixin,UpdateView):
    model = Plant_Harvest
    fields = '__all__'
    success_url = reverse_lazy('home')

class PlantHarvestDelete(LoginRequiredMixin,DeleteView):
    model = Plant_Harvest
    success_url = reverse_lazy('home')

class LabResultCreate(LoginRequiredMixin,CreateView):
    model = Lab_Result
    fields = '__all__'

class LabResultUpdate(LoginRequiredMixin,UpdateView):
    model = Lab_Result
    fields = '__all__'
    success_url = reverse_lazy('home')

class LabResultDelete(LoginRequiredMixin,DeleteView):
    model = Lab_Result
    success_url = reverse_lazy('home')

class LabSampleResultCreate(LoginRequiredMixin,CreateView):
    model = Lab_Sample_Result
    fields = '__all__'

class LabSampleResultUpdate(LoginRequiredMixin,UpdateView):
    model = Lab_Sample_Result
    fields = '__all__'
    success_url = reverse_lazy('home')

class LabSampleResultDelete(LoginRequiredMixin,DeleteView):
    model = Lab_Sample_Result
    success_url = reverse_lazy('home')

class LabSampleCreate(LoginRequiredMixin,CreateView):
    model = Lab_Sample
    fields = '__all__'

class LabSampleUpdate(LoginRequiredMixin,UpdateView):
    model = Lab_Sample
    fields = '__all__'
    success_url = reverse_lazy('home')

class LabSampleDelete(LoginRequiredMixin,DeleteView):
    model = Lab_Sample
    success_url = reverse_lazy('home')

class InventoryCreate(LoginRequiredMixin,CreateView):
    model = Inventory
    fields = '__all__'

class InventoryUpdate(LoginRequiredMixin,UpdateView):
    model = Inventory
    fields = '__all__'
    success_url = reverse_lazy('home')

class InventoryDelete(LoginRequiredMixin,DeleteView):
    model = Inventory
    success_url = reverse_lazy('home')

class InventoryRoomCreate(LoginRequiredMixin,CreateView):
    model = Inventory_Room
    fields = '__all__'

class InventoryRoomUpdate(LoginRequiredMixin,UpdateView):
    model = Inventory_Room
    fields = '__all__'
    success_url = reverse_lazy('home')

class InventoryRoomDelete(LoginRequiredMixin,DeleteView):
    model = Inventory_Room
    success_url = reverse_lazy('home')

class InventorySublotCreate(LoginRequiredMixin,CreateView):
    model = Inventory_Sublot
    fields = '__all__'

class InventorySublotUpdate(LoginRequiredMixin,UpdateView):
    model = Inventory_Sublot
    fields = '__all__'
    success_url = reverse_lazy('home')

class InventorySublotDelete(LoginRequiredMixin,DeleteView):
    model = Inventory_Sublot
    success_url = reverse_lazy('home')

class InventoryMoveCreate(LoginRequiredMixin,CreateView):
    model = Inventory_Move
    fields = '__all__'

class InventoryMoveUpdate(LoginRequiredMixin,UpdateView):
    model = Inventory_Move
    fields = '__all__'
    success_url = reverse_lazy('home')

class InventoryMoveDelete(LoginRequiredMixin,DeleteView):
    model = Inventory_Move
    success_url = reverse_lazy('home')

class PlantCureCreate(LoginRequiredMixin,CreateView):
    model = Plant_Cure
    fields = '__all__'

class PlantCureUpdate(LoginRequiredMixin,UpdateView):
    model = Plant_Cure
    fields = '__all__'
    success_url = reverse_lazy('home')

class PlantCureDelete(LoginRequiredMixin,DeleteView):
    model = Plant_Cure
    success_url = reverse_lazy('home')

class InvoiceInventoryCreate(LoginRequiredMixin,CreateView):
    model = Invoice_Inventory
    fields = '__all__'

class InvoiceInventoryUpdate(LoginRequiredMixin,UpdateView):
    model = Invoice_Inventory
    fields = '__all__'
    success_url = reverse_lazy('home')

class InvoiceInventoryDelete(LoginRequiredMixin,DeleteView):
    model = Invoice_Inventory
    success_url = reverse_lazy('home')

class InvoiceModelCreate(LoginRequiredMixin,CreateView):
    model = Invoice_Model
    fields = '__all__'

class InvoiceModelUpdate(LoginRequiredMixin,UpdateView):
    model = Invoice_Model
    fields = '__all__'
    success_url = reverse_lazy('home')

class InvoiceModelDelete(LoginRequiredMixin,DeleteView):
    model = Invoice_Model
    success_url = reverse_lazy('home')

class ManifestDriverCreate(LoginRequiredMixin,CreateView):
    model = Manifest_Driver
    fields = '__all__'

class ManifestDriverUpdate(LoginRequiredMixin,UpdateView):
    model = Manifest_Driver
    fields = '__all__'
    success_url = reverse_lazy('home')

class ManifestDriverDelete(LoginRequiredMixin,DeleteView):
    model = Manifest_Driver
    success_url = reverse_lazy('home')

class StopItemCreate(LoginRequiredMixin,CreateView):
    model = Stop_Item
    fields = '__all__'

class StopItemUpdate(LoginRequiredMixin,UpdateView):
    model = Stop_Item
    fields = '__all__'
    success_url = reverse_lazy('home')

class StopItemDelete(LoginRequiredMixin,DeleteView):
    model = Stop_Item
    success_url = reverse_lazy('home')

class ManifestStopCreate(LoginRequiredMixin,CreateView):
    model = Manifest_Stop
    fields = '__all__'

class ManifestStopUpdate(LoginRequiredMixin,UpdateView):
    model = Manifest_Stop
    fields = '__all__'
    success_url = reverse_lazy('home')

class ManifestStopDelete(LoginRequiredMixin,DeleteView):
    model = Manifest_Stop
    success_url = reverse_lazy('home')

class ManifestVehicleCreate(LoginRequiredMixin,CreateView):
    model = Manifest_Vehicle
    fields = '__all__'

class ManifestVehicleUpdate(LoginRequiredMixin,UpdateView):
    model = Manifest_Vehicle
    fields = '__all__'
    success_url = reverse_lazy('home')

class ManifestVehicleDelete(LoginRequiredMixin,DeleteView):
    model = Manifest_Vehicle
    success_url = reverse_lazy('home')

class ManifestThirdPartyTransporterCreate(LoginRequiredMixin,CreateView):
    model = Manifest_ThirdPartyTransporter
    fields = '__all__'

class ManifestThirdPartyTransporterUpdate(LoginRequiredMixin,UpdateView):
    model = Manifest_ThirdPartyTransporter
    fields = '__all__'
    success_url = reverse_lazy('home')

class ManifestThirdPartyTransporterDelete(LoginRequiredMixin,DeleteView):
    model = Manifest_ThirdPartyTransporter
    success_url = reverse_lazy('home')

class ManifestCreate(LoginRequiredMixin,CreateView):
    model = Manifest
    fields = '__all__'

class ManifestUpdate(LoginRequiredMixin,UpdateView):
    model = Manifest
    fields = '__all__'
    success_url = reverse_lazy('home')

class ManifestDelete(LoginRequiredMixin,DeleteView):
    model = Manifest
    success_url = reverse_lazy('home')

class GrowRoomCreate(LoginRequiredMixin,CreateView):
    model = Grow_Room
    fields = '__all__'

class GrowRoomUpdate(LoginRequiredMixin,UpdateView):
    model = Grow_Room
    fields = '__all__'
    success_url = reverse_lazy('home')

class GrowRoomDelete(LoginRequiredMixin,DeleteView):
    model = Grow_Room
    success_url = reverse_lazy('home')


# Archive vvvvvvvvvvvvvvvvv
class TTStorageBatchCreateView(LoginRequiredMixin,CreateView):
    form_class = forms.TTHarvestToStorageForm
    template_name = 'tracker/tt_harvest_to_storage_form.html'
    success_url = "home"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.weight_transfer()
        return super().form_valid(form)




# Detail Template Views
# =====================
class StrainDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = Strain

class TTInventoryDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = TT_Inventory

class TTInventoryProductDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = TT_Inventory_Product

class TTUserInfoDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = TT_User_Info

class TTLocationDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = TT_Location

class TTPlantBatchDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = TT_Plant_Batch

class TTPlantBatchHarvestDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = TT_Plant_Batch_Harvest

    def get_queryset(self):
        return TT_Plant_Batch_Harvest.objects.filter(user=self.request.user)

class TTStorageBatchDetailView(LoginRequiredMixin,generic.DetailView):
    """Generic class-based detail view."""
    model = TT_Storage_Batch

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



# List Template Views
# =====================

class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'

class PlantListView(ListView):
    model = Plant
    template_name = 'plant_list.html'