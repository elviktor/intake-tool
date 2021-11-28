from django.forms import ModelForm, CheckboxSelectMultiple, Select, HiddenInput
from .models import IntakeUser

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset

class IntakeUserForm(ModelForm):
    class Meta:
        model = IntakeUser
        fields = {'user', 'first_name', 'last_name', 'area', 'msc_group'}
        widgets = {
            'user': HiddenInput,
            'area': CheckboxSelectMultiple,
            'msc_group': CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(IntakeUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(

                'msc_group',
                'first_name',
                'last_name',
                'area'

            )
        )
        self.fields['user'].initial = self.request.user
