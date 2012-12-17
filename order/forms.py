# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from order.models import Order
from order.settings import PAYMENT_METHOD_CHOICES, DISPATCH_TIME_CHOICES, RECIEPT_TYPE_CHOICES

class OrderForm(ModelForm):
    reciept_type = forms.ChoiceField(label=_('Reciept Type'), widget=forms.RadioSelect(), choices=RECIEPT_TYPE_CHOICES)
    payment_method = forms.ChoiceField(label=_('Payment Method'), widget=forms.RadioSelect(), choices=PAYMENT_METHOD_CHOICES)
    dispatch_time = forms.ChoiceField(label=_('Dispatch Time'), widget=forms.RadioSelect(), choices=DISPATCH_TIME_CHOICES)
    uni_no = forms.IntegerField(label=_('Uni No.'), required=False, widget=forms.TextInput(attrs={'disabled': 'disabled'}))
    company_title = forms.CharField(label=_('Company Title'), required=False, widget=forms.TextInput(attrs={'disabled': 'disabled'}))

    class Meta:
        model = Order
        exclude = ('user', 'cart', 'status', 'total', 'voucher_code',
            'created_at', 'last_modified', 'items', 'dispatched_date', 'discount_total',
            'order_id', 'gross_total', 'net_total', 'billing_country', 'shipping_country')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field in self:
            if field.field.widget.__class__.__name__ == 'TextInput':
                field.field.widget.attrs['class'] = 'input-xxxlarge'
    """    
    def clean(self):
        if self.cleaned_data['reciept_type'] == 2:
            if self.cleand_data['uni_no'] and not self.cleaned_data['company_title']:
                raise forms.ValidationError(_('Please enter company title'))
            if self.cleaned_data['company_title'] and not self.cleaned_data['uni_no']:
                raise forms.ValidationError(_('Please enter uni no'))

        return self.cleaned_data
    """
    def clean_uni_no(self):
        if self.cleaned_data['uni_no'] and not self.data['company_title']:
            raise forms.ValidationError(_('Please enter company title'))
        return self.cleaned_data['uni_no']

    def clean_company_title(self):
        if self.cleaned_data['company_title'] and not self.data['uni_no']:
            raise forms.ValidationError(_('Please enter uni no'))
        return self.cleaned_data['company_title']

class OrderUpdateForm(ModelForm):
    class Meta:
        model = Order
        fields = ('status',)
