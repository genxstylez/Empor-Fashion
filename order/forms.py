from django import forms
from django.forms import ModelForm
from order.models import Order
from order.settings import PAYMENT_METHOD_CHOICES

class OrderForm(ModelForm):
    required_css_class = 'required'
    payment_method = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_METHOD_CHOICES)
    class Meta:
        model = Order
        exclude = ('user', 'cart', 'new', 'status', 'total', 
            'created_at', 'last_modified', 'items', 'dispatched_date', 'discount_total',
            'order_id', 'gross_total', 'net_total')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['shipping_country'].widget.attrs['id'] = 'ship_country'
        for field in self.fields:
            if field != 'payment_method' and field != 'shipping_country' and field != 'billing_country':
                self.fields[field].widget.attrs['class'] = 'input-xxxlarge'
