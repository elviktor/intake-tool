from django import forms
from django.forms.models import ModelForm
from django.forms import inlineformset_factory
from .models import Strain, TT_Location, TT_Sublot, TT_Plant_Batch, TT_Storage_Batch, TT_Product_Batch, TT_Lab_Sample, TT_Inventory, TT_Inventory_Product, Stop_Item, Invoice_Model, Invoice_Inventory, TT_Plant_Batch_Harvest,TT_Plant_Batch_Harvest_Delete, Lab_Sample_Result, Lab_Result


class TTHarvestToStorageForm(ModelForm):
   class Meta:
      model = TT_Storage_Batch
      fields = ['harvest_batch','package_number','location_date','location','sublot','from_row','to_row','wet_dry','produce_category','weight','status','converted','destroy_reason','destroy_reason_id','destroy_scheduled','destroy_scheduled_time','notes']
   
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
      fields = ['sample_name','product_batch','active','location','sublot','from_row','to_row','amount','amount_used','quantity','biotrack_id','inventory_id','inventory_type','lab_license','location_license','medical_grade','parent_id','result','results','rn_d','sample_use','session_time','test_results','transaction_id','notes']
   
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
      fields = ['inventory','product_batch','product_name','qa_status','total_quantity','remaining_quantity','total_amount','remaining_amount','unit_based','usable_weight','rec_usable_weight','med_usable_weight','medicated','seized','session_time','status','transaction_id','notes']
   
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

class TTInventoryToStopItemForm(ModelForm):
   class Meta:
      model = Stop_Item
      fields = ['inventory_product','description','biotrack_id','inventory_id','manifest_id','quantity','quantity_received','session_time','stop_number','transaction_id','weight']
   
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
      fields = ['invoice_model','inventory_product','product_name','amount','price','biotrack_id','inventory_id','invoice_id','transaction_id','uom']
   
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
      fields = ['sample_name','biotrack_id','lab_provided','sample_id','test_id','test_panel','test_pass','test_value','transaction_id']
   
   def __init__(self, *args, user, **kwargs):
      self.user = user
      super().__init__(*args, **kwargs)


class TTLocationCreateForm(ModelForm):
   class Meta:
      model = TT_Location
      fields = ['name','external_id','biotrack_id','location_license','quarantine','transaction_id','notes']
   
   def __init__(self, *args, user, **kwargs):
      self.user = user
      super().__init__(*args, **kwargs)
  

class TTSublotCreateForm(ModelForm):
   
   class Meta:
      model = TT_Sublot
      fields = ['sublot_name','location','amount','external_id','location_license','transaction_id','uom','notes']
   
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
      fields = ['birth_date','strain','quantity','location','sublot','from_row','to_row','mother','org_id','parent_id','room_id','converted','destroy_reason','destroy_reason_id','destroy_scheduled','destroy_scheduled_time','external_id','harvest_scheduled','session_time','state','transaction_id','notes']
   
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
      fields = ['deleted','plant_batch','location','sublot','from_row','to_row','harvest_stage','harvest_completed','harvest_start_date','harvest_finish_date','external_id','harvest_id','biotrack_id','transaction_id','total_wet_weight','total_dry_weight','notes']
   
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
      fields = ['inventory_name','inventory_type','location','sublot','from_row','to_row','external_id','biotrack_id','id_serial','location_license','notes']
   
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
      fields = ['invoice_name','inventory','accepted','buyer_location_license','invoice_id','location_license','refund_invoice_id','refunded','session_time','transaction_id','notes']
   
   def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['inventory'].queryset = TT_Inventory.objects.filter(user=self.user)

   inventory = forms.ModelChoiceField(queryset=TT_Inventory.objects.all(), empty_label="Select an inventory...")

InvoiceModelCreateFormsetA = inlineformset_factory(
    TT_Inventory, Invoice_Model, form=InvoiceModelCreateForm, fields=('inventory',), can_delete=True, extra=0)


# Delete Forms
# ===================================

class TTPlantBatchHarvestDeleteForm(ModelForm):
      class Meta:
         model = TT_Plant_Batch_Harvest_Delete
         exclude = ["delete_time"]
      
      def check_deleted(self):
         deleted = self.instance.TT_Plant_Batch_Harvest.deleted

         # Ensure that selected item has not already been deleted quantity is not greater than total batch quantity
         if deleted == True:
            raise forms.ValidationError("Item already deleted.")

         else: pass