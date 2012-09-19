from django import forms
from django.utils.translation import ugettext_lazy as _
from userena.forms import SignupFormOnlyEmail, EditProfileForm, identification_field_factory
from member.settings import COUNTRY_CHOICES
from member.models import UserProfile
from userena.utils import get_profile_model
from userena import settings as userena_settings
from django.contrib.auth import authenticate

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

class ProfileForm(EditProfileForm):
    """ Base form used for fields that are always required """
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

    def __init__(self, *args, **kw):
        super(EditProfileForm, self).__init__(*args, **kw)
        # Put the first and last name at the top
        new_order = self.fields.keyOrder[:-2]
        new_order.insert(0, 'first_name')
        new_order.insert(1, 'last_name')
        self.fields.keyOrder = new_order

    class Meta:
        model = get_profile_model()
        exclude = ['user', 'mugshot', 'privacy']

    def save(self, force_insert=False, force_update=False, commit=True):
        profile = super(EditProfileForm, self).save(commit=commit)
        # Save first and last name
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        return profile

class AuthenticationForm(forms.Form):
    
    attrs_dict = {'class': 'required input-large'}
    # userena siginform override for css class

    identification = forms.CharField(label=_('Email'), widget=forms.TextInput(attrs=attrs_dict), max_length=75,
                    error_messages={'required': _('Please supply your email')})
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs=attrs_dict, render_value=False))
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(), required=False,
                label=_(u'Remember me') % {'days': _(userena_settings.USERENA_REMEMBER_ME_DAYS[0])})

    def clean(self):
        identification = self.cleaned_data.get('identification')
        password = self.cleaned_data.get('password')

        if identification and password:
            user = authenticate(identification=identification, password=password)
            if user is None:
                raise forms.ValidationError(_(u"Please enter a correct username or email and password. Note that both fields are case-sensitive."))
        return self.cleaned_data
