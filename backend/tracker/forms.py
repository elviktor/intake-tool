from django import forms
from django.forms.models import ModelForm
from .models import TT_Storage_Batch


class TTStorageBatchForm(ModelForm):
   class Meta:
      model = TT_Storage_Batch
      fields = ['weight']
   
   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['weight'].widget.attrs.update.update({'step': '0.01'})
   
   def clean_product_weight(self):
        weight = self.cleaned_data['weight']
        total_weight = self.instance.TT_Plant_Batch_Harvest.remaining_dry_weight

        # Ensure that product weight is not greater than total weight
        if weight > total_weight:
            raise forms.ValidationError("Product weight cannot be greater than total weight.")

        return weight
