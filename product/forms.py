from django import forms
from product.models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product

class ProductGroupForm(forms.ModelForm):
    class Meta:
        model = ProductGroup

class OptionGroupForm(forms.ModelForm):
    class Meta:
        model = OptionGroup

