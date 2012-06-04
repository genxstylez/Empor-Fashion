from django import forms
from product.models import *

#TYPE_CHOICES = [(0, '----')]
#TYPE_CHOICES += [(type.id, type.name) for type in ProductVariationType.objects.all()]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product

class ProductGroupForm(forms.ModelForm):
    class Meta:
        model = ProductGroup

class OptionGroupForm(forms.ModelForm):
    class Meta:
        model = OptionGroup

