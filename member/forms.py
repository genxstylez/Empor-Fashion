from django import forms
from django.utils.translation import ugettext_lazy as _
from userena.forms import SignupFormOnlyEmail
from member.settings import COUNTRY_CHOICES
from member.models import UserProfile

class RegisterForm(SignupFormOnlyEmail):
    first_name = forms.CharField(label=_('First name'), max_length=30, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    last_name = forms.CharField(label=_('Last name'), max_length=30, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    phone = forms.CharField(label=_('Phone'), max_length=50, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    billing_recipient = forms.CharField(label=_('Recipient'), max_length=100, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    billing_street1 = forms.CharField(label=_('Street 1'), max_length=100, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    billing_street2 = forms.CharField(label=_('Street 2'), max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    billing_city = forms.CharField(label=_('City'), max_length=100, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    billing_post_code = forms.CharField(label=_('Post Code'), max_length=100, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    billing_country = forms.ChoiceField(label=_('Country'), choices=COUNTRY_CHOICES) 
    shipping_recipient = forms.CharField(label=_('Recipient'), max_length=100, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    shipping_street1 = forms.CharField(label=_('Street 1'), max_length=100, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    shipping_street2 = forms.CharField(label=_('Street 2'), max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    shipping_city = forms.CharField(label=_('City'), max_length=100, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    shipping_post_code = forms.CharField(label=_('Post Code'), max_length=100, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    shipping_country = forms.ChoiceField(label=_('Country'), choices=COUNTRY_CHOICES)
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'input-xxxlarge'
        self.fields['password1'].widget.attrs['class'] = 'input-xxxlarge'
        self.fields['password2'].widget.attrs['class'] = 'input-xxxlarge'
    
    def save(self):
        new_user = super(RegisterForm, self).save()
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()
        
        try:
            profile = UserProfile.objects.get(user=new_user)
        except UserProfile.DoesNotExit:
            profile = UserProfile(user=new_user)

        profile.billing_recipient = self.cleaned_data['billing_recipient']
        profile.billing_street1 = self.cleaned_data['billing_street1']

        if self.cleaned_data['billing_street2']:
            profile.billing_street2 = self.cleaned_data['billing_street2']

        profile.billing_city = self.cleaned_data['billing_city']
        profile.billing_post_code = self.cleaned_data['billing_post_code']
        profile.billing_country = self.cleaned_data['billing_country']
        profile.shipping_recipient = self.cleaned_data['shipping_recipient']
        profile.shipping_street1 = self.cleaned_data['shipping_street1']

        if self.cleaned_data['shipping_street2']:
            profile.shipping_street2 = self.cleaned_data['shipping_street2']

        profile.shipping_city = self.cleaned_data['shipping_city']
        profile.shipping_post_code = self.cleaned_data['shipping_post_code']
        profile.shipping_country = self.cleaned_data['shipping_country']

        profile.save()

        return new_user
