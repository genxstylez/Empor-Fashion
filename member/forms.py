# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import auth
from django.contrib.auth.models import User
from member.settings import COUNTRY_CHOICES, RESERVED_KEYWORD
from member.models import UserTemp
import re

class RegisterForm(forms.ModelForm):
    username = forms.CharField(min_length=3, max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())
    passconf = forms.CharField(label=_('Confrim password'), widget=forms.PasswordInput())

    class Meta:
        model = UserTemp
        exclude = ('activation_code', 'activated')
        widgets = {
            'birthday': forms.DateInput(format='%Y/%m/%d', attrs={'class': 'birthday' }),
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'shipping_country' or field == 'billing_country' or field == 'birthday':
                pass
            else:
                self.fields[field].widget.attrs['class'] = 'input-xxxlarge'
        new_order = self.fields.keyOrder[:-1]
        new_order.insert(2, 'passconf')
        self.fields.keyOrder = new_order

    def clean_username(self):
        # 限制使用者帳號格式
        if not re.match('^[a-zA-Z]{1}[a-zA-Z0-9_]{2,15}$', self.cleaned_data['username']):
            raise forms.ValidationError(_('username can only contain english, numbers and underscore. \
                Begin with character only.'))

        # 檢查是否已經有帳號存在
        if self.cleaned_data['username'] in RESERVED_KEYWORD:
            raise forms.ValidationError(_('this username is not allowed'))
        elif User.objects.filter(username=self.cleaned_data['username']):
            raise forms.ValidationError(_('this username has been registered'))

        return self.cleaned_data['username']

    def clean_password(self):
        # 限制密碼格式
        if not re.match('\S{3,12}', self.cleaned_data['password']):
            raise forms.ValidationError(_('this password is not valid'))

        return self.cleaned_data['password']

    def clean_passconf(self):
        password = self.cleaned_data.get('password', None)
        passconf = self.cleaned_data.get('passconf')

        if password:
            if passconf != password:
                raise forms.ValidationError(_('Password confirm not equal to password'))

        return self.cleaned_data['passconf']

    def clean_email(self):
        # 檢查是否已有相同 email
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_('This email address is already in use. Please supply another email address.'))
        elif UserTemp.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already registered and waiting for activate. \
                Please activate directly and doesn't need to register again."))
        return self.cleaned_data['email']   
 
class ProfileForm(forms.Form):
    first_name = forms.CharField(label=_('First name'), max_length=30, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    last_name = forms.CharField(label=_('Last name'), max_length=30, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    phone = forms.CharField(label=_('Phone'), max_length=50, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    billing_recipient = forms.CharField(label=_('Billing Recipient'), max_length=100, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    billing_street1 = forms.CharField(label=_('Street 1'), max_length=100, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    billing_street2 = forms.CharField(label=_('Street 2'), max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    billing_city = forms.CharField(label=_('City'), max_length=100, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    billing_post_code = forms.CharField(label=_('Post Code'), max_length=100, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    billing_country = forms.ChoiceField(label=_('Country'), choices=COUNTRY_CHOICES)
    shipping_recipient = forms.CharField(label=_('Shipping Recipient'), max_length=100, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    shipping_street1 = forms.CharField(label=_('Street 1'), max_length=100, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    shipping_street2 = forms.CharField(label=_('Street 2'), max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    shipping_city = forms.CharField(label=_('City'), max_length=100, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    shipping_post_code = forms.CharField(label=_('Post Code'), max_length=100, widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    shipping_country = forms.ChoiceField(label=_('Country'), choices=COUNTRY_CHOICES)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label=_('Account'), 
        widget=forms.TextInput(attrs={'class': 'input-xlarge'}) 
    )
    password = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'class': 'input-xlarge'}), 
        label=_('password')
    )
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label=_('Remember me'))
    def clean_username(self):
        if UserTemp.objects.filter(username__iexact=self.cleaned_data['username']).count() == 0 and \
        User.objects.filter(username__iexact=self.cleaned_data['username']).count() == 0:
            raise forms.ValidationError(_('Account cannot be found, please register'))
        return self.cleaned_data['username']

class ReActivateForm(forms.Form):
    username = forms.CharField(widget=forms.HiddenInput)
    email = forms.EmailField()

    def clean_email(self):
        user = User.objects.filter(email=self.cleaned_data['email'])
        if user.count() >= 1:
            raise forms.ValidationError(_('there is another user register with this email'))

        usertemp = UserTemp.objects.filter(email=self.cleaned_data['email'])
        usertemp = usertemp.exclude(username=self.cleaned_data['username'])
        if usertemp.count() >= 1:
            raise forms.ValidationError(_('there is another user register with this email'))

        return self.cleaned_data['email']

class FacebookBindingForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'rel': _('Account'), 'class': 'input-xlarge', 'placeholder': _('Account')}))
    password = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'rel': _('Password'), 'class': 'input-xlarge', 'placeholder': _('Password')}))

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if not user:
                message = _('Please enter correct username and password')
                self._errors['password'] = self.error_class([message])

                del cleaned_data['password']

        return cleaned_data
