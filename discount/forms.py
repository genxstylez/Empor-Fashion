from django import forms
from discount.models import Discount

class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
