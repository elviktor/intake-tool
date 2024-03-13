from django import forms
from django.forms.models import ModelForm
from django.forms import inlineformset_factory
from .models import Strain, TT_Location, TT_Sublot, TT_Plant_Batch, TT_Storage_Batch, TT_Product_Batch, TT_Lab_Sample, TT_Inventory, TT_Inventory_Product, Stop_Item, Invoice_Model, Invoice_Inventory, TT_Plant_Batch_Harvest, Lab_Sample_Result, Lab_Result, TT_Location_Delete,TT_Sublot_Delete,Strain_Delete,TT_Plant_Batch_Delete,TT_Plant_Batch_Harvest_Delete,TT_Storage_Batch_Delete,TT_Product_Batch_Delete,Lab_Result_Delete,Lab_Sample_Result_Delete,TT_Lab_Sample_Delete,TT_Inventory_Delete,TT_Inventory_Product_Delete,Invoice_Model_Delete,Invoice_Inventory_Delete, TT_User_Info, Manifest_Driver, Manifest_Stop, Manifest_Vehicle, Manifest_ThirdPartyTransporter, Manifest, Manifest_Stop_Delete,Manifest_Driver_Delete,Manifest_Vehicle_Delete,Manifest_ThirdPartyTransporter_Delete,Manifest_Delete

# Date and Time Widgets
class DateInput(forms.DateInput):
    input_type = 'date'

class DateTimeInput(forms.DateTimeInput):
   input_type = 'datetime'

class TimeInput(forms.TimeInput):
   input_type = 'time'


class TTHarvestToStorageForm(ModelForm):
   class Meta:
      model = TT_Storage_Batch
      fields = ['harvest_batch','package_number','location_date','location','sublot','from_row','to_row','wet_dry','produce_category','weight','status','converted','destroy_reason','destroy_reason_id','destroy_scheduled','destroy_scheduled_time','notes']
      widgets = {
            'location_date': DateInput(),
            'destroy_scheduled_time': DateTimeInput(),
        }
   
   def __init__(self, *args, user, **kwargs):
       self.user = user
       super().__init__(*args, **kwargs)
       self.fields['weight'].widget.attrs.update({'step': '0.01'})

       self.fields['harvest_batch'].queryset = TT_Plant_Batch_Harvest.objects.filter(user=self.user)
       self.fields['location'].queryset = TT_Location.objects.filter(user=self.user)
       self.fields['sublot'].queryset = TT_Sublot.objects.filter(user=self.user)
   
   def clean_product_weight(self):
        weight = self.cleaned_data['weight']
        total_weight = self.instance.TT_Plant_Batch_Harvest.remaining_dry_weight

        # Ensure that product weight is not greater than total weight
        if weight > total_weight:
            raise forms.ValidationError("Product weight cannot be greater than total weight.")

        return weight
   
   harvest_batch = forms.ModelChoiceField(queryset=TT_Plant_Batch_Harvest.objects.all(), empty_label="Select a harvest...")
   location = forms.ModelChoiceField(queryset=TT_Location.objects.all(), empty_label="Select a location...")
   sublot = forms.ModelChoiceField(queryset=TT_Sublot.objects.all(), empty_label="Select a sublot...") 

TTHarvestToStorageFormsetA = inlineformset_factory(
    TT_Plant_Batch_Harvest, TT_Storage_Batch, form=TTHarvestToStorageForm, fields=('harvest_batch',), can_delete=True, extra=0)
TTHarvestToStorageFormsetB = inlineformset_factory(
    TT_Location, TT_Storage_Batch, form=TTHarvestToStorageForm, fields=('location',), can_delete=True, extra=0)
TTHarvestToStorageFormsetC = inlineformset_factory(
    TT_Sublot, TT_Storage_Batch, form=TTHarvestToStorageForm, fields=('sublot',), can_delete=True, extra=0)
   

class TTStorageToProductForm(ModelForm):
   class Meta:
      model = TT_Product_Batch
      fields = ['product_name','product_category','harvest_batch','storage_batches','location','sublot','from_row','to_row','uom','total_quantity','total_weight', 'available','wet_dry','packaging','wholesale_price','msrp','moq','thc_percent','terp_percent','thc_mg','thc_mg_per_serving','grow_type','description','sell_points','expiration_date','use_by_date','sku','coa','tested','notes']
      widgets = {
            'expiration_date': DateInput(),
            'use_by_date': DateInput(),
        }


   def __init__(self, *args, user, **kwargs):
      self.user = user
      super().__init__(*args, **kwargs)

      self.fields['harvest_batch'].queryset = TT_Plant_Batch_Harvest.objects.filter(user=self.user)
      self.fields['storage_batches'].queryset = TT_Storage_Batch.objects.filter(user=self.user)
      self.fields['location'].queryset = TT_Location.objects.filter(user=self.user)
      self.fields['sublot'].queryset = TT_Sublot.objects.filter(user=self.user)

   harvest_batch = forms.ModelChoiceField(queryset=TT_Plant_Batch_Harvest.objects.all(), empty_label="Select a harvest batch...")
   storage_batches = forms.ModelChoiceField(queryset=TT_Storage_Batch.objects.all(), empty_label="Select a storage batch...")
   location = forms.ModelChoiceField(queryset=TT_Location.objects.all(), empty_label="Select a location...")
   sublot = forms.ModelChoiceField(queryset=TT_Sublot.objects.all(), empty_label="Select a sublot...")

TTStorageToProductFormsetA = inlineformset_factory(
    TT_Plant_Batch_Harvest, TT_Product_Batch, form=TTStorageToProductForm, fields=('harvest_batch',), can_delete=True, extra=0)
TTStorageToProductFormsetB = inlineformset_factory(
    TT_Storage_Batch, TT_Product_Batch, form=TTStorageToProductForm, fields=('storage_batches',), can_delete=True, extra=0)
TTStorageToProductFormsetC = inlineformset_factory(
    TT_Location, TT_Product_Batch, form=TTStorageToProductForm, fields=('location',), can_delete=True, extra=0)
TTStorageToProductFormsetD = inlineformset_factory(
    TT_Sublot, TT_Product_Batch, form=TTStorageToProductForm, fields=('sublot',), can_delete=True, extra=0)

class TTProductToLabSampleForm(ModelForm):
   class Meta:
      model = TT_Lab_Sample
      fields = ['sample_name','product_batch','active','location','sublot','from_row','to_row','amount','amount_used','quantity','inventory_id','inventory_type','lab_license','location_license','medical_grade','parent_id','result','results','rn_d','sample_use','test_results','notes']
   
   def __init__(self, *args, user, **kwargs):
       self.user = user
       super().__init__(*args, **kwargs)

       self.fields['amount'].widget.attrs.update({'step': '0.01'})

       self.fields['product_batch'].queryset = TT_Product_Batch.objects.filter(user=self.user)
       self.fields['location'].queryset = TT_Location.objects.filter(user=self.user)
       self.fields['sublot'].queryset = TT_Sublot.objects.filter(user=self.user)
       self.fields['results'].queryset = Lab_Result.objects.filter(user=self.user)
       self.fields['test_results'].queryset = Lab_Sample_Result.objects.filter(user=self.user)


   def clean_sample_weight(self):
      weight = self.cleaned_data['amount']
      total_weight = self.instance.TT_Product_Batch.remaining_weight

        # Ensure that product weight is not greater than total weight
      if weight > total_weight:
         raise forms.ValidationError("Sample weight cannot be greater than total product weight.")

      return weight

   def clean_sample_quantity(self):
      quantity = self.cleaned_data['quantity']
      total_quantity = self.instance.TT_Product_Batch.remaining_quantity

      # Ensure that product weight is not greater than total weight
      if quantity > total_quantity:
          raise forms.ValidationError("Sample quantity cannot be greater than total product quantity.")

      return quantity
   
   product_batch = forms.ModelChoiceField(queryset=TT_Product_Batch.objects.all(), empty_label="Select a product...")
   location = forms.ModelChoiceField(queryset=TT_Location.objects.all(), empty_label="Select a location...")
   sublot = forms.ModelChoiceField(queryset=TT_Sublot.objects.all(), empty_label="Select a sublot...")
   results = forms.ModelChoiceField(queryset=Lab_Result.objects.all(), empty_label="Select a lab result...")
   test_results = forms.ModelChoiceField(queryset=Lab_Sample_Result.objects.all(), empty_label="Select a lab sample result...")

TTProductToLabSampleFormsetA = inlineformset_factory(
    TT_Product_Batch, TT_Lab_Sample, form=TTProductToLabSampleForm, fields=('product_batch',), can_delete=True, extra=0)
TTProductToLabSampleFormsetB = inlineformset_factory(
    TT_Location, TT_Lab_Sample, form=TTProductToLabSampleForm, fields=('location',), can_delete=True, extra=0)
TTProductToLabSampleFormsetC = inlineformset_factory(
    TT_Sublot, TT_Lab_Sample, form=TTProductToLabSampleForm, fields=('sublot',), can_delete=True, extra=0)
TTProductToLabSampleFormsetD = inlineformset_factory(
    Lab_Result, TT_Lab_Sample, form=TTProductToLabSampleForm, fields=('results',), can_delete=True, extra=0)
TTProductToLabSampleFormsetE = inlineformset_factory(
    Lab_Sample_Result, TT_Lab_Sample, form=TTProductToLabSampleForm, fields=('test_results',), can_delete=True, extra=0)

   
# I need to split Inventory Creation and then Adding items/products to Inventory (foreign key)
class TTProductToInventoryForm(ModelForm):
   class Meta:
      model = TT_Inventory_Product
      fields = ['inventory','product_batch','qa_status','total_quantity','total_amount','unit_based','usable_weight','rec_usable_weight','med_usable_weight','medicated','seized','status','notes']
   
   def __init__(self, *args, user, **kwargs):
       self.user = user
       super().__init__(*args, **kwargs)
       
       self.fields['total_amount'].widget.attrs.update({'step': '0.01'})

       self.fields['inventory'].queryset = TT_Inventory.objects.filter(user=self.user)
       self.fields['product_batch'].queryset = TT_Product_Batch.objects.filter(user=self.user)
   
   def clean_sample_weight(self):
      weight = self.cleaned_data['total_amount']
      total_weight = self.instance.TT_Product_Batch.remaining_weight

        # Ensure that product weight is not greater than total weight
      if weight > total_weight:
         raise forms.ValidationError("Inventory item weight cannot be greater than total product weight.")

      return weight

   def clean_sample_quantity(self):
      quantity = self.cleaned_data['total_quantity']
      total_quantity = self.instance.TT_Product_Batch.remaining_quantity

      # Ensure that inventory product quantity is not greater than total batch quantity
      if quantity > total_quantity:
          raise forms.ValidationError("Inventory item quantity cannot be greater than total product quantity.")

      return quantity
   
   inventory = forms.ModelChoiceField(queryset=TT_Inventory.objects.all(), empty_label="Select an inventory...")
   product_batch = forms.ModelChoiceField(queryset=TT_Product_Batch.objects.all(), empty_label="Select a product batch...")

TTProductToInventoryFormsetA = inlineformset_factory(
    TT_Inventory, TT_Inventory_Product, form=TTProductToInventoryForm, fields=('inventory',), can_delete=True, extra=0)
TTProductToInventoryFormsetB = inlineformset_factory(
    TT_Product_Batch, TT_Inventory_Product, form=TTProductToInventoryForm, fields=('product_batch',), can_delete=True, extra=0)

# Used instead of a StopItemCreateForm
class TTInventoryToStopItemForm(ModelForm):
   class Meta:
      model = Stop_Item
      fields = ['stop_number','inventory_product','description','quantity_received','weight']
   
   def __init__(self, *args, user, **kwargs):
       self.user = user
       super().__init__(*args, **kwargs)

       self.fields['weight'].widget.attrs.update({'step': '0.01'})

       self.fields['inventory_product'].queryset = TT_Inventory_Product.objects.filter(user=self.user)
   
   def clean_sample_weight(self):
      weight = self.cleaned_data['weight']
      total_weight = self.instance.TT_Inventory_Product.remaining_weight

        # Ensure that product weight is not greater than total weight
      if weight > total_weight:
         raise forms.ValidationError("Stop Item weight cannot be greater than total product weight.")

      return weight

   def clean_sample_quantity(self):
      quantity = self.cleaned_data['quantity']
      total_quantity = self.instance.TT_Inventory_Product.remaining_quantity

      # Ensure that stop item quantity is not greater than total batch quantity
      if quantity > total_quantity:
          raise forms.ValidationError("Stop Item quantity cannot be greater than total product quantity.")

      return quantity
   
   inventory_product = forms.ModelChoiceField(queryset=TT_Inventory_Product.objects.all(), empty_label="Select an inventory product...")
   
TTInventoryToStopItemFormsetA = inlineformset_factory(
    TT_Inventory_Product, Stop_Item, form=TTProductToInventoryForm, fields=('inventory_product',), can_delete=True, extra=0)


class TTInventoryToInvoiceItemForm(ModelForm):
   class Meta:
      model = Invoice_Inventory
      fields = ['invoice_model','inventory_product','product_name','amount','price','inventory_id','uom']
   
   def __init__(self, *args, user, **kwargs):
      self.user = user
      super().__init__(*args, **kwargs)

      self.fields['amount'].widget.attrs.update({'step': '0.01'})

      self.fields['invoice_model'].queryset = Invoice_Model.objects.filter(user=self.user)
      self.fields['inventory_product'].queryset = TT_Inventory_Product.objects.filter(user=self.user)


   def clean_sample_quantity(self):
      quantity = self.cleaned_data['amount']
      total_quantity = self.instance.TT_Inventory_Product.remaining_quantity

      # Ensure that stop item quantity is not greater than total batch quantity
      if quantity > total_quantity:
         raise forms.ValidationError("Stop Item quantity cannot be greater than total product quantity.")

      return quantity
   
   invoice_model = forms.ModelChoiceField(queryset=Invoice_Model.objects.all(), empty_label="Select an invoice...")
   inventory_product = forms.ModelChoiceField(queryset=TT_Inventory_Product.objects.all(), empty_label="Select an inventory product...")

TTInventoryToInvoiceItemFormsetA = inlineformset_factory(
    Invoice_Model, Invoice_Inventory, form=TTInventoryToInvoiceItemForm, fields=('invoice_model',), can_delete=True, extra=0)
TTInventoryToInvoiceItemFormsetB = inlineformset_factory(
    TT_Inventory_Product, Invoice_Inventory, form=TTInventoryToInvoiceItemForm, fields=('inventory_product',), can_delete=True, extra=0)
      

# Custom User-Only Model Create Forms
# ===================================

class StrainCreateForm(ModelForm):
   class Meta:
      model = Strain
      fields = ['name','shortname','source','type','status','coa_link','thc_amt','cbd_amt','notes']
   
   def __init__(self, *args, user, **kwargs):
      self.user = user
      super().__init__(*args, **kwargs)


class LabResultCreateForm(ModelForm):
   class Meta:
      model = Lab_Result
      fields = ['name','sample_id','failure','test','uom','value']
   
   def __init__(self, *args, user, **kwargs):
      self.user = user
      super().__init__(*args, **kwargs)


class LabSampleResultCreateForm(ModelForm):
   class Meta:
      model = Lab_Sample_Result
      fields = ['sample_name','lab_provided','sample_id','test_id','test_panel','test_pass','test_value','transaction_id']
   
   def __init__(self, *args, user, **kwargs):
      self.user = user
      super().__init__(*args, **kwargs)


class TTUserInfoCreateForm(ModelForm):
   class Meta:
      model = TT_User_Info
      fields = ['company_name','company_ocm_license','contact_first_name','contact_last_name','contact_email','contact_phone','contact_website','contact_address','contact_city','contact_state','contact_zip','notes']
   
   def __init__(self, *args, user, **kwargs):
      self.user = user
      super().__init__(*args, **kwargs)


class TTLocationCreateForm(ModelForm):
   class Meta:
      model = TT_Location
      fields = ['name','external_id','location_license','quarantine','notes']
   
   def __init__(self, *args, user, **kwargs):
      self.user = user
      super().__init__(*args, **kwargs)
  

class TTSublotCreateForm(ModelForm):
   
   class Meta:
      model = TT_Sublot
      fields = ['sublot_name','location','rows','amount','external_id','location_license','uom','notes']
   
   def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['location'].queryset = TT_Location.objects.filter(user=self.user)

   location = forms.ModelChoiceField(queryset=TT_Location.objects.all(), empty_label="Select a location...") 
   # added this for styling purposes only, the queryset arguement here doesn't appear to do anything given the presence of the queryset in the __init__ function, although including the queryset here seems to be required to get the code to work

TTSublotCreateFormset = inlineformset_factory(
    TT_Location, TT_Sublot, form=TTSublotCreateForm, fields=('location',), can_delete=True, extra=0)


class TTPlantBatchCreateForm(ModelForm):
   
   class Meta:
      model = TT_Plant_Batch
      fields = ['birth_date','strain','quantity','location','sublot','from_row','to_row','mother','org_id','parent_id','converted','destroy_reason','destroy_scheduled','destroy_scheduled_time','harvest_scheduled','notes']
      widgets = {
            'birth_date': DateInput(),
            'destroy_scheduled_time': DateInput(),
        }
   
   def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['strain'].queryset = Strain.objects.filter(user=self.user)
        self.fields['location'].queryset = TT_Location.objects.filter(user=self.user)
        self.fields['sublot'].queryset = TT_Sublot.objects.filter(user=self.user)

   strain = forms.ModelChoiceField(queryset=Strain.objects.all(), empty_label="Select a strain...")
   location = forms.ModelChoiceField(queryset=TT_Location.objects.all(), empty_label="Select a location...")
   sublot = forms.ModelChoiceField(queryset=TT_Sublot.objects.all(), empty_label="Select a sublot...") 
   # added this for styling purposes only, the queryset arguement here doesn't appear to do anything given the presence of the queryset in the __init__ function, although including the queryset here seems to be required to get the code to work

TTPlantBatchCreateFormsetA = inlineformset_factory(
    Strain, TT_Plant_Batch, form=TTPlantBatchCreateForm, fields=('strain',), can_delete=True, extra=0)
TTPlantBatchCreateFormsetB = inlineformset_factory(
    TT_Location, TT_Plant_Batch, form=TTPlantBatchCreateForm, fields=('location',), can_delete=True, extra=0)
TTPlantBatchCreateFormsetC = inlineformset_factory(
    TT_Sublot, TT_Plant_Batch, form=TTPlantBatchCreateForm, fields=('sublot',), can_delete=True, extra=0)


class TTPlantBatchHarvestCreateForm(ModelForm):
   
   class Meta:
      model = TT_Plant_Batch_Harvest
      fields = ['deleted','plant_batch','location','sublot','from_row','to_row','harvest_stage','harvest_completed','harvest_start_date','harvest_finish_date','total_wet_weight','total_dry_weight','notes']
      widgets = {
            'harvest_start_date': DateInput(),
            'harvest_finish_date': DateInput()
        }
   
   def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['plant_batch'].queryset = TT_Plant_Batch.objects.filter(user=self.user)
        self.fields['location'].queryset = TT_Location.objects.filter(user=self.user)
        self.fields['sublot'].queryset = TT_Sublot.objects.filter(user=self.user)

   plant_batch = forms.ModelChoiceField(queryset=TT_Plant_Batch.objects.all(), empty_label="Select a plant batch...") 
   location = forms.ModelChoiceField(queryset=TT_Location.objects.all(), empty_label="Select a location...") 
   sublot = forms.ModelChoiceField(queryset=TT_Sublot.objects.all(), empty_label="Select a sublot...") 
   # added this for styling purposes only, the queryset arguement here doesn't appear to do anything given the presence of the queryset in the __init__ function, although including the queryset here seems to be required to get the code to work

TTPlantBatchHarvestCreateFormsetA = inlineformset_factory(
    TT_Plant_Batch, TT_Plant_Batch_Harvest, form=TTPlantBatchHarvestCreateForm, fields=('plant_batch',), can_delete=True, extra=0)
TTPlantBatchHarvestCreateFormsetB = inlineformset_factory(
    TT_Location, TT_Plant_Batch_Harvest, form=TTPlantBatchHarvestCreateForm, fields=('location',), can_delete=True, extra=0)
TTPlantBatchHarvestCreateFormsetC = inlineformset_factory(
    TT_Sublot, TT_Plant_Batch_Harvest, form=TTPlantBatchHarvestCreateForm, fields=('sublot',), can_delete=True, extra=0)


class TTInventoryCreateForm(ModelForm):
   
   class Meta:
      model = TT_Inventory
      fields = ['inventory_name','inventory_type','location','sublot','from_row','to_row','external_id','id_serial','location_license','notes']
   
   def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['location'].queryset = TT_Location.objects.filter(user=self.user)
        self.fields['sublot'].queryset = TT_Sublot.objects.filter(user=self.user)

   location = forms.ModelChoiceField(queryset=TT_Location.objects.all(), empty_label="Select a location...") 
   sublot = forms.ModelChoiceField(queryset=TT_Sublot.objects.all(), empty_label="Select a sublot...") 

TTInventoryCreateFormsetA = inlineformset_factory(
    TT_Location, TT_Inventory, form=TTInventoryCreateForm, fields=('location',), can_delete=True, extra=0)
TTInventoryCreateFormsetB = inlineformset_factory(
    TT_Sublot, TT_Inventory, form=TTInventoryCreateForm, fields=('sublot',), can_delete=True, extra=0)


class InvoiceModelCreateForm(ModelForm):
   
   class Meta:
      model = Invoice_Model
      fields = ['invoice_name','inventory','accepted','buyer_location_license','location_license','refund_invoice_id','refunded','notes']
   
   def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['inventory'].queryset = TT_Inventory.objects.filter(user=self.user)

   inventory = forms.ModelChoiceField(queryset=TT_Inventory.objects.all(), empty_label="Select an inventory...")

InvoiceModelCreateFormsetA = inlineformset_factory(
    TT_Inventory, Invoice_Model, form=InvoiceModelCreateForm, fields=('inventory',), can_delete=True, extra=0)


class ManifestDriverCreateForm(ModelForm):
   
   class Meta:
      model = Manifest_Driver
      fields = ['dateof_birth','name','notes']
      widgets = {
            'dateof_birth': DateInput(),
        }
   
   def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        

class StopItemCreateForm(ModelForm):
   
   class Meta:
      model = Stop_Item
      fields = ['inventory_product','description','inventory_id','manifest_id','quantity','quantity_received','stop_number','weight','notes']
   
   def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['inventory_product'].queryset = TT_Inventory_Product.objects.filter(user=self.user)

   inventory_product = forms.ModelChoiceField(queryset=TT_Inventory_Product.objects.all(), empty_label="Select an inventory product...")

StopItemCreateFormsetA = inlineformset_factory(
    TT_Inventory_Product, Stop_Item, form=StopItemCreateForm, fields=('inventory_product',), can_delete=True, extra=0)


class ManifestStopCreateForm(ModelForm):
   
   class Meta:
      model = Manifest_Stop
      fields = ['stop_name','stop_number','items','approximate_departure','approximate_arrival','approximate_route','driver_arrived','driver_arrived_time','invoice','biotrack_invoice_id','location_license','manifest_id','notes']
      widgets = {
            'approximate_arrival': DateInput(),
            'approximate_departure': DateInput(),
            'driver_arrived_time': TimeInput()
        }
   
   def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['items'].queryset = Stop_Item.objects.filter(user=self.user)
        self.fields['invoice'].queryset = Invoice_Model.objects.filter(user=self.user)

   items = forms.ModelChoiceField(queryset=Stop_Item.objects.all(), empty_label="Select a stop item...")

ManifestStopCreateFormsetA = inlineformset_factory(
    Stop_Item, Manifest_Stop, form=ManifestStopCreateForm, fields=('items',), can_delete=True, extra=0)
ManifestStopCreateFormsetB = inlineformset_factory(
    Invoice_Model, Manifest_Stop, form=ManifestStopCreateForm, fields=('invoice',), can_delete=True, extra=0)


class ManifestVehicleCreateForm(ModelForm):
   
   class Meta:
      model = Manifest_Vehicle
      fields = ['description','vehicle_name','notes']
   
   def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
       

class ManifestThirdPartyTransporterCreateForm(ModelForm):
   
   class Meta:
      model = Manifest_ThirdPartyTransporter
      fields = ['license_number', 'name', 'notes']
   
   def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)


class ManifestCreateForm(ModelForm):
   
   class Meta:
      model = Manifest
      fields = ['manifest_name','destination_category','stops','stop_count','total_item_count','type','name','phone','street','city','state','zip','drivers','vehicle','third_party_transporter','created_on','completed','completion_date','driver_arrived','in_transit','is_accepted','is_parked','received','updated_on','notes']
      widgets = {
            'created_on': DateInput(),
        }
   
   def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['stops'].queryset = Manifest_Stop.objects.filter(user=self.user)
        self.fields['drivers'].queryset = Manifest_Driver.objects.filter(user=self.user)
        self.fields['third_party_transporter'].queryset = Manifest_ThirdPartyTransporter.objects.filter(user=self.user)
        self.fields['vehicle'].queryset = Manifest_Vehicle.objects.filter(user=self.user)

   stops = forms.ModelChoiceField(queryset=Manifest_Stop.objects.all(), empty_label="Select a stop...")
   drivers = forms.ModelChoiceField(queryset=Manifest_Driver.objects.all(), empty_label="Select a driver...")
   third_party_transporter = forms.ModelChoiceField(queryset=Manifest_ThirdPartyTransporter.objects.all(), empty_label="Select a third party transporter...") 
   vehicle = forms.ModelChoiceField(queryset=Manifest_Vehicle.objects.all(), empty_label="Select a vehicle...") 
   

ManifestCreateFormsetA = inlineformset_factory(
    Manifest_Stop, Manifest, form=ManifestCreateForm, fields=('stops',), can_delete=True, extra=0)
ManifestCreateFormsetB = inlineformset_factory(
    Manifest_Driver, Manifest, form=ManifestCreateForm, fields=('drivers',), can_delete=True, extra=0)
ManifestCreateFormsetC = inlineformset_factory(
    Manifest_ThirdPartyTransporter, Manifest, form=ManifestCreateForm, fields=('third_party_transporter',), can_delete=True, extra=0)
ManifestCreateFormsetD = inlineformset_factory(
    Manifest_Vehicle, Manifest, form=ManifestCreateForm, fields=('vehicle',), can_delete=True, extra=0)



# Delete Forms
# ===================================

class TTLocationDeleteForm(ModelForm):
      class Meta:
         model = TT_Location_Delete
         fields = ['deleted_item','notes']
      
      def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['deleted_item'].queryset = TT_Location.objects.filter(user=self.user)

      def check_deleted(self):
         deleted = self.instance.TT_Location.deleted

         # Ensure that selected item has not already been deleted
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass
      
      deleted_item = forms.ModelChoiceField(queryset=TT_Location.objects.all(), empty_label="Select a batch to delete...")

TTLocationDeleteFormsetA = inlineformset_factory(
    TT_Location, TT_Location_Delete, form=TTLocationDeleteForm, fields=('deleted_item',), can_delete=True, extra=0)


class TTSublotDeleteForm(ModelForm):
      class Meta:
         model = TT_Sublot_Delete
         fields = ['deleted_item','notes']
      
      def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['deleted_item'].queryset = TT_Sublot.objects.filter(user=self.user)

      def check_deleted(self):
         deleted = self.instance.TT_Sublot.deleted

         # Ensure that selected item has not already been deleted
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass
      
      deleted_item = forms.ModelChoiceField(queryset=TT_Sublot.objects.all(), empty_label="Select a batch to delete...")

TTSublotDeleteFormsetA = inlineformset_factory(
    TT_Sublot, TT_Sublot_Delete, form=TTSublotDeleteForm, fields=('deleted_item',), can_delete=True, extra=0)


class StrainDeleteForm(ModelForm):
      class Meta:
         model = Strain_Delete
         fields = ['deleted_item','notes']
      
      def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['deleted_item'].queryset = Strain.objects.filter(user=self.user)

      def check_deleted(self):
         deleted = self.instance.Strain.deleted

         # Ensure that selected item has not already been deleted
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass
      
      deleted_item = forms.ModelChoiceField(queryset=Strain.objects.all(), empty_label="Select a batch to delete...")

StrainDeleteFormsetA = inlineformset_factory(
    Strain, Strain_Delete, form=StrainDeleteForm, fields=('deleted_item',), can_delete=True, extra=0)


class TTPlantBatchDeleteForm(ModelForm):
      class Meta:
         model = TT_Plant_Batch_Delete
         fields = ['deleted_item','notes']
      
      def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['deleted_item'].queryset = TT_Plant_Batch.objects.filter(user=self.user)

      def check_deleted(self):
         deleted = self.instance.TT_Plant_Batch.deleted

         # Ensure that selected item has not already been deleted
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass
      
      deleted_item = forms.ModelChoiceField(queryset=TT_Plant_Batch.objects.all(), empty_label="Select a batch to delete...")

TTPlantBatchDeleteFormsetA = inlineformset_factory(
    TT_Plant_Batch, TT_Plant_Batch_Delete, form=TTPlantBatchDeleteForm, fields=('deleted_item',), can_delete=True, extra=0)

class TTPlantBatchHarvestDeleteForm(ModelForm):
      class Meta:
         model = TT_Plant_Batch_Harvest_Delete
         fields = ['deleted_item','notes']
      
      def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['deleted_item'].queryset = TT_Plant_Batch_Harvest.objects.filter(user=self.user)

      def check_deleted(self):
         deleted = self.instance.TT_Plant_Batch_Harvest.deleted

         # Ensure that selected item has not already been deleted
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass
      
      deleted_item = forms.ModelChoiceField(queryset=TT_Plant_Batch_Harvest.objects.all(), empty_label="Select a batch to delete...")

TTPlantBatchHarvestDeleteFormsetA = inlineformset_factory(
    TT_Plant_Batch_Harvest, TT_Plant_Batch_Harvest_Delete, form=TTPlantBatchHarvestDeleteForm, fields=('deleted_item',), can_delete=True, extra=0)


class TTStorageBatchDeleteForm(ModelForm):
      class Meta:
         model = TT_Storage_Batch_Delete
         fields = ['deleted_item','notes']
      
      def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['deleted_item'].queryset = TT_Storage_Batch.objects.filter(user=self.user)

      def check_deleted(self):
         deleted = self.instance.TT_Storage_Batch.deleted

         # Ensure that selected item has not already been deleted
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass
      
      deleted_item = forms.ModelChoiceField(queryset=TT_Storage_Batch.objects.all(), empty_label="Select a batch to delete...")

TTStorageBatchDeleteFormsetA = inlineformset_factory(
    TT_Storage_Batch, TT_Storage_Batch_Delete, form=TTStorageBatchDeleteForm, fields=('deleted_item',), can_delete=True, extra=0)


class TTProductBatchDeleteForm(ModelForm):
      class Meta:
         model = TT_Product_Batch_Delete
         fields = ['deleted_item','notes']
      
      def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['deleted_item'].queryset = TT_Product_Batch.objects.filter(user=self.user)

      def check_deleted(self):
         deleted = self.instance.TT_Product_Batch.deleted

         # Ensure that selected item has not already been deleted
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass
      
      deleted_item = forms.ModelChoiceField(queryset=TT_Product_Batch.objects.all(), empty_label="Select a batch to delete...")

TTProductBatchDeleteFormsetA = inlineformset_factory(
    TT_Product_Batch, TT_Product_Batch_Delete, form=TTProductBatchDeleteForm, fields=('deleted_item',), can_delete=True, extra=0)


class LabResultDeleteForm(ModelForm):
      class Meta:
         model = Lab_Result_Delete
         fields = ['deleted_item','notes']
      
      def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['deleted_item'].queryset = Lab_Result.objects.filter(user=self.user)

      def check_deleted(self):
         deleted = self.instance.Lab_Result.deleted

         # Ensure that selected item has not already been deleted
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass
      
      deleted_item = forms.ModelChoiceField(queryset=Lab_Result.objects.all(), empty_label="Select a batch to delete...")

LabResultDeleteFormsetA = inlineformset_factory(
    Lab_Result, Lab_Result_Delete, form=LabResultDeleteForm, fields=('deleted_item',), can_delete=True, extra=0)


class LabSampleResultDeleteForm(ModelForm):
      class Meta:
         model = Lab_Sample_Result_Delete
         fields = ['deleted_item','notes']
      
      def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['deleted_item'].queryset = Lab_Sample_Result.objects.filter(user=self.user)

      def check_deleted(self):
         deleted = self.instance.Lab_Sample_Result.deleted

         # Ensure that selected item has not already been deleted
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass
      
      deleted_item = forms.ModelChoiceField(queryset=Lab_Sample_Result.objects.all(), empty_label="Select a batch to delete...")

LabSampleResultDeleteFormsetA = inlineformset_factory(
    Lab_Sample_Result, Lab_Sample_Result_Delete, form=LabSampleResultDeleteForm, fields=('deleted_item',), can_delete=True, extra=0)


class TTLabSampleDeleteForm(ModelForm):
      class Meta:
         model = TT_Lab_Sample_Delete
         fields = ['deleted_item','notes']
      
      def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['deleted_item'].queryset = TT_Lab_Sample.objects.filter(user=self.user)

      def check_deleted(self):
         deleted = self.instance.TT_Lab_Sample.deleted

         # Ensure that selected item has not already been deleted
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass
      
      deleted_item = forms.ModelChoiceField(queryset=TT_Lab_Sample.objects.all(), empty_label="Select a batch to delete...")

TTLabSampleDeleteFormsetA = inlineformset_factory(
    TT_Lab_Sample, TT_Lab_Sample_Delete, form=TTLabSampleDeleteForm, fields=('deleted_item',), can_delete=True, extra=0)


class TTInventoryDeleteForm(ModelForm):
      class Meta:
         model = TT_Inventory_Delete
         fields = ['deleted_item','notes']
      
      def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['deleted_item'].queryset = TT_Inventory.objects.filter(user=self.user)

      def check_deleted(self):
         deleted = self.instance.TT_Inventory.deleted

         # Ensure that selected item has not already been deleted
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass
      
      deleted_item = forms.ModelChoiceField(queryset=TT_Inventory.objects.all(), empty_label="Select a batch to delete...")

TTInventoryDeleteFormsetA = inlineformset_factory(
    TT_Inventory, TT_Inventory_Delete, form=TTInventoryDeleteForm, fields=('deleted_item',), can_delete=True, extra=0)


class TTInventoryProductDeleteForm(ModelForm):
      class Meta:
         model = TT_Inventory_Product_Delete
         fields = ['deleted_item','notes']
      
      def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['deleted_item'].queryset = TT_Inventory_Product.objects.filter(user=self.user)

      def check_deleted(self):
         deleted = self.instance.TT_Inventory_Product.deleted

         # Ensure that selected item has not already been deleted
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass
      
      deleted_item = forms.ModelChoiceField(queryset=TT_Inventory_Product.objects.all(), empty_label="Select a batch to delete...")

TTInventoryProductDeleteFormsetA = inlineformset_factory(
    TT_Inventory_Product, TT_Inventory_Product_Delete, form=TTInventoryProductDeleteForm, fields=('deleted_item',), can_delete=True, extra=0)


class InvoiceModelDeleteForm(ModelForm):
      class Meta:
         model = Invoice_Model_Delete
         fields = ['deleted_item','notes']
      
      def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['deleted_item'].queryset = Invoice_Model.objects.filter(user=self.user)

      def check_deleted(self):
         deleted = self.instance.Invoice_Model.deleted

         # Ensure that selected item has not already been deleted
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass
      
      deleted_item = forms.ModelChoiceField(queryset=Invoice_Model.objects.all(), empty_label="Select a batch to delete...")

InvoiceModelDeleteFormsetA = inlineformset_factory(
    Invoice_Model, Invoice_Model_Delete, form=InvoiceModelDeleteForm, fields=('deleted_item',), can_delete=True, extra=0)


class InvoiceInventoryDeleteForm(ModelForm):
      class Meta:
         model = Invoice_Inventory_Delete
         fields = ['deleted_item','notes']
      
      def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['deleted_item'].queryset = Invoice_Inventory.objects.filter(user=self.user)

      def check_deleted(self):
         deleted = self.instance.Invoice_Inventory.deleted

         # Ensure that selected item has not already been deleted
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass
      
      deleted_item = forms.ModelChoiceField(queryset=Invoice_Inventory.objects.all(), empty_label="Select a batch to delete...")

InvoiceInventoryDeleteFormsetA = inlineformset_factory(
    Invoice_Inventory, Invoice_Inventory_Delete, form=InvoiceInventoryDeleteForm, fields=('deleted_item',), can_delete=True, extra=0)


class ManifestDriverDeleteForm(ModelForm):
      class Meta:
         model = Manifest_Driver_Delete
         fields = ['deleted_item','notes']
      
      def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['deleted_item'].queryset = Manifest_Driver.objects.filter(user=self.user)

      def check_deleted(self):
         deleted = self.instance.Manifest_Driver.deleted

         # Ensure that selected item has not already been deleted
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass
      
      deleted_item = forms.ModelChoiceField(queryset=Manifest_Driver.objects.all(), empty_label="Select a batch to delete...")

ManifestDriverDeleteFormsetA = inlineformset_factory(
    Manifest_Driver, Manifest_Driver_Delete, form=ManifestDriverDeleteForm, fields=('deleted_item',), can_delete=True, extra=0)

class ManifestStopDeleteForm(ModelForm):
      class Meta:
         model = Manifest_Stop_Delete
         fields = ['deleted_item','notes']
      
      def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['deleted_item'].queryset = Manifest_Stop.objects.filter(user=self.user)

      def check_deleted(self):
         deleted = self.instance.Manifest_Stop.deleted

         # Ensure that selected item has not already been deleted
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass
      
      deleted_item = forms.ModelChoiceField(queryset=Manifest_Stop.objects.all(), empty_label="Select a batch to delete...")

ManifestStopDeleteFormsetA = inlineformset_factory(
    Manifest_Stop, Manifest_Stop_Delete, form=ManifestStopDeleteForm, fields=('deleted_item',), can_delete=True, extra=0)


class ManifestVehicleDeleteForm(ModelForm):
      class Meta:
         model = Manifest_Vehicle_Delete
         fields = ['deleted_item','notes']
      
      def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['deleted_item'].queryset = Manifest_Vehicle.objects.filter(user=self.user)

      def check_deleted(self):
         deleted = self.instance.Manifest_Vehicle.deleted

         # Ensure that selected item has not already been deleted
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass
      
      deleted_item = forms.ModelChoiceField(queryset=Manifest_Vehicle.objects.all(), empty_label="Select a batch to delete...")

ManifestVehicleDeleteFormsetA = inlineformset_factory(
    Manifest_Vehicle, Manifest_Vehicle_Delete, form=ManifestVehicleDeleteForm, fields=('deleted_item',), can_delete=True, extra=0)


class ManifestThirdPartyTransporterDeleteForm(ModelForm):
      class Meta:
         model = Manifest_ThirdPartyTransporter_Delete
         fields = ['deleted_item','notes']
      
      def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['deleted_item'].queryset = Manifest_ThirdPartyTransporter.objects.filter(user=self.user)

      def check_deleted(self):
         deleted = self.instance.Manifest_ThirdPartyTransporter.deleted

         # Ensure that selected item has not already been deleted
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass
      
      deleted_item = forms.ModelChoiceField(queryset=Manifest_ThirdPartyTransporter.objects.all(), empty_label="Select a batch to delete...")

ManifestThirdPartyTransporterDeleteFormsetA = inlineformset_factory(
    Manifest_ThirdPartyTransporter, Manifest_ThirdPartyTransporter_Delete, form=ManifestThirdPartyTransporterDeleteForm, fields=('deleted_item',), can_delete=True, extra=0)


class ManifestDeleteForm(ModelForm):
      class Meta:
         model = Manifest_Delete
         fields = ['deleted_item','notes']
      
      def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['deleted_item'].queryset = Manifest.objects.filter(user=self.user)

      def check_deleted(self):
         deleted = self.instance.Manifest.deleted

         # Ensure that selected item has not already been deleted
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass
      
      deleted_item = forms.ModelChoiceField(queryset=Manifest.objects.all(), empty_label="Select a batch to delete...")

ManifestDeleteFormsetA = inlineformset_factory(
    Manifest, Manifest_Delete, form=ManifestDeleteForm, fields=('deleted_item',), can_delete=True, extra=0)



