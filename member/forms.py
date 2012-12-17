# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import auth
from django.contrib.auth.models import User
from member.settings import RESERVED_KEYWORD
from member.models import UserTemp, UserProfile
import re

class RegisterForm(forms.ModelForm):
    username = forms.CharField(min_length=3, max_length=20, label=_('Username'))
    password = forms.CharField(widget=forms.PasswordInput(), label=_('Password'))
    passconf = forms.CharField(label=_('Confrim password'), widget=forms.PasswordInput())
    birthday = forms.DateField(label=_('Birthday'), input_formats=['%Y/%m/%d',], \
        widget=forms.DateInput(attrs={'class': 'birthday', 'data-date-format': 'yyyy/mm/dd'}))
    post_code = forms.CharField(label=_('Post Code'), widget=forms.TextInput(attrs={'class': 'input-small', 'placeholder': _('Post Code')}))
    phone = forms.CharField(label=_('Phone'), widget=forms.TextInput(attrs={'class': 'input-large'}))
    address = forms.CharField(label=_('Address'), widget=forms.TextInput(attrs={'class': 'input-xxlarge'}))
    tos = forms.BooleanField(widget=forms.CheckboxInput())

    class Meta:
        model = UserTemp
        exclude = ('activation_code', 'country')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field in ['post_code', 'birthday', 'gender', 'address', 'phone']:
                pass
            else:
                self.fields[field].widget.attrs['class'] = 'input-xxxlarge'
        new_order = self.fields.keyOrder[:-1]
        new_order.insert(2, 'passconf')
        self.fields.keyOrder = new_order

    def clean_tos(self):
        if not self.cleaned_data['tos']:
            raise forms.ValidationError(_('You must agree TOS to register'))

        return self.cleaned_data['tos']

    def clean_username(self):
        if not re.match('^[a-zA-Z]{1}[a-zA-Z0-9_]{2,15}$', self.cleaned_data['username']):
            raise forms.ValidationError(_('username can only contain english, numbers and underscore. \
                Begin with character only.'))

        if self.cleaned_data['username'] in RESERVED_KEYWORD:
            raise forms.ValidationError(_('this username is not allowed'))
        elif User.objects.filter(username=self.cleaned_data['username']):
            raise forms.ValidationError(_('this username has been registered'))

        return self.cleaned_data['username']

    def clean_password(self):
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
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_('This email address is already in use. Please supply another email address.'))
        elif UserTemp.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already registered and waiting for activate. \
                Please activate directly and doesn't need to register again."))
        return self.cleaned_data['email']   
 
class ProfileForm(forms.ModelForm):
	birthday = forms.DateField(label=_('Birthday'), input_formats=['%Y/%m/%d',], \
		widget=forms.DateInput(attrs={'class': 'birthday', 'data-date-format': 'yyyy/mm/dd'}))
	post_code = forms.CharField(label=_('Post Code'), widget=forms.TextInput(attrs={'class': 'input-small', 'placeholder': _('Post Code')}))

	class Meta:
		model = UserProfile
		exclude = ('reset_code', 'user', 'country', 'tos')

	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			if field in ['birthday', 'gender', 'post_code']:
				pass
			else:
				self.fields[field].widget.attrs['class'] = 'input-xxxlarge' 

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
            raise forms.ValidationError(_('This email address is already in use. Please supply another email address.'))

        usertemp = UserTemp.objects.filter(email=self.cleaned_data['email'])
        usertemp = usertemp.exclude(username=self.cleaned_data['username'])
        if usertemp.count() >= 1:
            raise forms.ValidationError(_('This email address is already in use. Please supply another email address.'))

        return self.cleaned_data['email']

class FacebookBindingForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'input-xlarge'}), label=_('Account'))
    password = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'input-xlarge'}), label=_('Password'))

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

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label=_('Old Password'), max_length=16, widget=forms.PasswordInput(attrs={'class': 'input-xxlarge'}))
    new_password = forms.CharField(label=_('New Password'), max_length=16, widget=forms.PasswordInput(attrs={'class': 'input-xxlarge'}))
    passconf = forms.CharField(label=_('Confirm password'), max_length=16, widget=forms.PasswordInput(attrs={'class': 'input-xxlarge'}))
    
    def clean_old_password(self):
        if not re.match('\S{3,12}', self.cleaned_data['old_password']):
            raise forms.ValidationError(_('this password is not valid'))

        return self.cleaned_data['old_password']

    def clean_new_password(self):
        if not re.match('\S{3,12}', self.cleaned_data['new_password']):
            raise forms.ValidationError(_('this password is not valid'))

        return self.cleaned_data['new_password']

    def clean_passconf(self):
        new_password = self.cleaned_data.get('new_password', None)
        passconf = self.cleaned_data.get('passconf')

        if new_password:
            if passconf != new_password:
                raise forms.ValidationError(_('Password does not match'))

        return self.cleaned_data['passconf']

class ResetPasswordForm(forms.Form):
    password = forms.CharField(label=_('New Password'), max_length=16, widget=forms.PasswordInput(attrs={'class': 'input-xxlarge'}))
    passconf = forms.CharField(label=_('Confirm Password'), max_length=16, widget=forms.PasswordInput(attrs={'class': 'input-xxlarge'}))
    
    def clean_password(self):
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

class ForgotPasswordForm(forms.Form):
    value = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-xlarge'}), label=_('Account or Email'))
