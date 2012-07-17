from django import forms
from django.forms import ModelForm
from order.models import Order
from order.settings import PAYMENT_METHOD_CHOICES

class OrderForm(ModelForm):
    payment_method = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_METHOD_CHOICES)
    class Meta:
        model = Order
        exclude = ('user', 'cart', 'new', 'status', 'total', 'created_at', 'last_modified')
