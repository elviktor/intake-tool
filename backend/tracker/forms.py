from django import forms
from django.forms.models import ModelForm
from .models import TT_Storage_Batch, TT_Product_Batch, TT_Lab_Sample, TT_Inventory_Product, Stop_Item


class TTHarvestToStorageForm(ModelForm):
   class Meta:
      model = TT_Storage_Batch
      fields = '__all__'
   
   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['weight'].widget.attrs.update({'step': '0.01'})
   
   def clean_product_weight(self):
        weight = self.cleaned_data['weight']
        total_weight = self.instance.TT_Plant_Batch_Harvest.remaining_dry_weight

        # Ensure that product weight is not greater than total weight
        if weight > total_weight:
            raise forms.ValidationError("Product weight cannot be greater than total weight.")

        return weight
   

class TTStorageToProductForm(ModelForm):
   class Meta:
      model = TT_Product_Batch
      fields = '__all__'


class TTProductToLabSampleForm(ModelForm):
   class Meta:
      model = TT_Lab_Sample
      fields = '__all__'
   
   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['amount'].widget.attrs.update({'step': '0.01'})
   
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
   
# I need to split Inventory Creation and then Adding items/products to Inventory (foreign key)
class TTProductToInventoryForm(ModelForm):
   class Meta:
      model = TT_Inventory_Product
      fields = '__all__'
   
   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['total_amount'].widget.attrs.update({'step': '0.01'})
   
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
   

class TTInventoryToStopItemForm(ModelForm):
   class Meta:
      model = Stop_Item
      fields = '__all__'
   
   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['weight'].widget.attrs.update({'step': '0.01'})
   
   def clean_sample_weight(self):
      weight = self.cleaned_data['weight']
      total_weight = self.instance.TT_Product_Batch.remaining_weight

        # Ensure that product weight is not greater than total weight
      if weight > total_weight:
         raise forms.ValidationError("Stop Item weight cannot be greater than total product weight.")

      return weight

   def clean_sample_quantity(self):
      quantity = self.cleaned_data['quantity']
      total_quantity = self.instance.TT_Product_Batch.remaining_quantity

      # Ensure that stop item quantity is not greater than total batch quantity
      if quantity > total_quantity:
          raise forms.ValidationError("Stop Item quantity cannot be greater than total product quantity.")

      return quantity
   
