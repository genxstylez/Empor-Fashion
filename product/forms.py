from django import forms
from product.models import *

TYPE_CHOICES = [(0, '----')]
TYPE_CHOICES += [(type.id, type.name) for type in ProductVariationType.objects.all()]

class ProductForm(forms.ModelForm):
    variation_type = forms.ChoiceField(required=True, choices=TYPE_CHOICES)
    variations = forms.ChoiceField(required=False)

    def clean_variations(self):
        if self.cleaned_data['variation_type'] == 0 and not self.cleaned_data['variations']:
            raise forms.ValidationError(_('Variations required'))

        return self.cleaned_data['variations']
         
    class Meta:
        model = Product
