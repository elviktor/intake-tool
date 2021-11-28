from django.forms import ModelForm, CheckboxSelectMultiple, Select
from .models import IntakeUser

class IntakeUserForm(ModelForm):
    class Meta:
        model = IntakeUser
        fields = '__all__'
        widgets = {
            'status': Select,
            'area': CheckboxSelectMultiple,
            'msc_group': CheckboxSelectMultiple,
        }
