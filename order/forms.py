# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from order.models import Order
from order.settings import PAYMENT_METHOD_CHOICES, DISPATCH_TIME_CHOICES, RECIEPT_TYPE_CHOICES

class OrderForm(ModelForm):
    required_css_class = 'required'
    reciept_type = forms.ChoiceField(widget=forms.RadioSelect(), choices=RECIEPT_TYPE_CHOICES)
    payment_method = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_METHOD_CHOICES)
    dispatch_time = forms.ChoiceField(widget=forms.RadioSelect(), choices=DISPATCH_TIME_CHOICES)

    class Meta:
        model = Order
        exclude = ('user', 'cart', 'new', 'status', 'total', 
            'created_at', 'last_modified', 'items', 'dispatched_date', 'discount_total',
            'order_id', 'gross_total', 'net_total')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field in self:
            if field.field.widget.__class__.__name__ == 'TextInput':
                field.field.widget.attrs['class'] = 'input-xxxlarge'

    def clean_uni_no(self):
        if self.cleaned_data['uni_no'] and not self.data['company_title']:
            raise forms.ValidationError(_('Please enter company title'))
        return self.cleaned_data['uni_no']

    def clean_company_title(self):
        if self.cleaned_data['company_title'] and not self.cleaned_data['uni_no']:
            raise forms.ValidationError(_('Please enter uni no'))
        return self.cleaned_data['company_title']
