# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.sites.models import Site
from django import forms
from member.models import UserProfile, UserTemp, ExtendedProfile, UserTalent, NewsPaper, EmailTemp, UserPreference
from member.settings import GENDER_CHOICES, TAIWAN_AREA, CHINA_AREA, HK_AREA, MISC_AREA
from member.settings import AESTHETICS_TYPE, MUSIC_TYPE, FRIENDSHIP_TYPE, JOB_CHOICES
from member.settings import JOB_TITLE_CHOICES, EDUCATION_CHOICES, MUSIC_TALENT_CHOICES
from member.settings import VIDEO_TALENT_CHOICES, DESIGN_TALENT_CHOICES, ART_TALENT_CHOICES
from member.settings import DANCE_TALENT_CHOICES, PERFORM_TALENT_CHOICES, TEXT_TALENT_CHOICES
from member.settings import LANGUAGE_TALENT_CHOICES, ELSE_TALENT_CHOICES, HABITAT_CHOICES
from member.settings import HKUSE_HABITAT_CHOICES, ACCOUNT_TYPE_CHOICES
from captcha.fields import CaptchaField
from svapp.field import YearMonthDayField
from svapp.widget import YearMonthDayWidget
from member.settings import RESERVED_KEYWORD
import re
from django.forms.extras.widgets import SelectDateWidget
import datetime

site = Site.objects.get_current()

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('username'), 'class': 'input-xxlarge'}), min_length=3, max_length=20, label=_('Username'))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('password'), 'class': 'input-xxlarge'}), label=_('Password'))
    passconf = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('confirm password'), 'class': 'input-xxlarge'}), label=_('confirm password'))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': _('email'), 'class': 'input-xxlarge'}), label=_('email'))
    nickname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('nickname'),'class': 'input-xxlarge'}), max_length=100, label=_('nick name'))
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs={'required': True}), label=_('Terms of service'))
    """ 
    birthday = YearMonthDayField(label=_('birthday'), widget=YearMonthDayWidget)
    habitat = forms.IntegerField(required=True)
    captcha_code = CaptchaField(label=_('captcha code'))
    taiwan_area = forms.ChoiceField(choices=TAIWAN_AREA, required=False)
    china_area = forms.ChoiceField(choices=CHINA_AREA, required=False)
    hk_area = forms.ChoiceField(choices=HK_AREA, required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect, label=_('gender'))
    misc_area = forms.ChoiceField(choices=MISC_AREA, required=False)
    """

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

        # 檢查待驗證帳號是否已經存在
        if UserTemp.objects.filter(username=self.cleaned_data['username']):
            raise forms.ValidationError(_('this username has been registered and waiting for activate'))

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

    def clean_nickname(self):
        # 檢查是否已有相同暱稱
        try:
            if UserProfile.objects.filter(nickname=self.cleaned_data['nickname']):
                raise forms.ValidationError(_('this nickname has been used'))
        except UserProfile.DoesNotExist:
            pass

        return self.cleaned_data['nickname']

    def clean_email(self):
        # 檢查是否已有相同 email
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_('This email address is already in use. Please supply another email address.'))
        elif UserTemp.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already registered and waiting for activate. \
                Please activate directly and doesn't need to register again."))
        elif EmailTemp.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is waiting for verifying."))
        return self.cleaned_data['email']


    """def clean_taiwan_area(self):
        habitat = self.cleaned_data.get('habitat')
        taiwan_area = self.cleaned_data['taiwan_area']
        if habitat == 1 and taiwan_area == '':
            raise forms.ValidationError(_('Please select the area you live'))
            
        return taiwan_area

    def clean_hk_area(self):
        habitat = self.cleaned_data.get('habitat')
        hk_area = self.cleaned_data['hk_area']
        if habitat == 3 and hk_area == '':
            raise forms.ValidationError(_('Please select the area you live'))
            
        return hk_area

    def clean_china_area(self):
        habitat = self.cleaned_data.get('habitat')
        china_area = self.cleaned_data['china_area']
        if habitat == 2 and china_area == '':
            raise forms.ValidationError(_('Please select the area you live'))
            
        return china_area

    def clean_misc_area(self):
        habitat = self.cleaned_data.get('habitat')
        misc_area = self.cleaned_data['misc_area']
        if habitat == 4 and misc_area == '':
            raise forms.ValidationError(_('Please select the area you live'))
            
        return misc_area"""

class ExtendedProfileForm(forms.ModelForm):
    height = forms.IntegerField(widget=forms.TextInput(attrs={'size':10}), required=False, label=_('Height'))
    weight = forms.IntegerField(widget=forms.TextInput(attrs={'size':10}), required=False, label=_('Weight'))
    aesthetics_type = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, 
        choices=AESTHETICS_TYPE, label=_('Aesthetics type'))
    music_type = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, 
        choices=MUSIC_TYPE, label=_('Music type'))
    friendship_type = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, 
        choices=FRIENDSHIP_TYPE, label=_('Friendship type'))
    interest_intro = forms.CharField(widget=forms.Textarea(attrs={'cols':100, 'rows':10}), required=False)
    self_intro = forms.CharField(widget=forms.Textarea(attrs={'cols':100, 'rows':10}), 
        required=False, label=_('Self introduction'))
    else_intro = forms.CharField(widget=forms.Textarea(attrs={'cols':100, 'rows':10}), required=False, label=_('Else'))
    custom_aesthetics_type = forms.CharField(widget=forms.TextInput(attrs={'size':8}), max_length=30, required=False)
    custom_music_type = forms.CharField(widget=forms.TextInput(attrs={'size':8}), max_length=30, required=False)
    custom_friendship_type = forms.CharField(widget=forms.TextInput(attrs={'size':8}), max_length=30, required=False)
    class Meta:
        model = ExtendedProfile
        exclude = ('user', 'fans_amount', 'gifts_amount', 'invite_amount', 'new_fans', 'new_gift', 
            'new_gb_message', 'blog_space', 'non_member_message', 'last_time_in_giftbox', )

    def clean_height(self):
        height = self.cleaned_data['height']

        if not height:
            return None

        if height > 1000:
            raise forms.ValidationError("Hey man, that funny, but please try again.")

        return height

    def clean_weight(self):
        weight = self.cleaned_data['weight']

        if not weight:
            return None

        if weight > 1000:
            raise forms.ValidationError("Hey man, that funny, but please try again.")

        return weight

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label=_('account'), widget=forms.TextInput(attrs={'class': 'input-xlarge', 'placeholder': _('account')}))
    password = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'input-xlarge', 'placeholder': _('password')}), label=_('password'))
    
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

class HKReActivateForm(forms.Form):
    username = forms.CharField(widget=forms.HiddenInput)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input-xxlarge'}))

    def clean_email(self):
        user = User.objects.filter(email=self.cleaned_data['email'])
        if user.count() >= 1:
            raise forms.ValidationError(_('there is another user register with this email'))

        usertemp = UserTemp.objects.filter(email=self.cleaned_data['email'])
        usertemp = usertemp.exclude(username=self.cleaned_data['username'])
        if usertemp.count() >= 1:
            raise forms.ValidationError(_('there is another user register with this email'))

        return self.cleaned_data['email']

class ProfileForm(forms.Form):
    realname = forms.CharField(required=False, max_length=30, label=_('Real name'))
    nickname = forms.CharField(max_length=20, label=_('Nick name'), widget=forms.TextInput(attrs={'size':30}))
    new_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'size':30}), label=_('Password'))
    new_passconf = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'size':30}), label=_('Confirm'))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect, label=_('Gender'))
    birthday = forms.CharField(required=False, label=_('Birthday'))
    cellphone = forms.CharField(required=False, label=_('Cellphone'), widget=forms.TextInput(attrs={'size':30}))
    telephone = forms.CharField(required=False, label=_('Telephone'), widget=forms.TextInput(attrs={'size':30}))
    get_sms = forms.BooleanField(required=False, label=_('I would like to recieve SMS or MMS information'))
    job = forms.ChoiceField(required=False, choices=JOB_CHOICES, label=_('Job'))
    job_title = forms.ChoiceField(required=False, choices=JOB_TITLE_CHOICES, label=_('Job title'))
    education = forms.ChoiceField(required=False, choices=EDUCATION_CHOICES, label=_('Education'))
    habitat = forms.ChoiceField(choices=HABITAT_CHOICES, label=_('habitat'), required=True)
    city = forms.CharField(label=_('city'), required=False, max_length=50, widget=forms.TextInput())
    address = forms.CharField(required=False, max_length=255, label=_('Address'), 
        widget=forms.TextInput(attrs={'size':80}))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(ProfileForm, self).__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = self.cleaned_data
        new_password = cleaned_data.get('new_password')
        new_passconf = cleaned_data.get('new_passconf')

        from django.forms.util import ErrorList
        if new_password != new_passconf:
            msg = _('verify password field is different from password feld')
            self._errors['new_passconf'] = ErrorList([msg])

        return cleaned_data


class DefaultProfileImageForm(forms.Form):
    file = forms.ImageField()

class UserTalentForm(forms.ModelForm):
    music_talent = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, 
        choices=MUSIC_TALENT_CHOICES, label=_('Music Talent'))
    video_talent = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, 
        choices=VIDEO_TALENT_CHOICES, label=_('Video Talent'))
    design_talent = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, 
        choices=DESIGN_TALENT_CHOICES, label=_('Design Talent'))
    art_talent = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, 
        choices=ART_TALENT_CHOICES, label=_('Art Talent'))
    dance_talent = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, 
        choices=DANCE_TALENT_CHOICES, label=_('Dance Talent'))
    perform_talent = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, 
        choices=PERFORM_TALENT_CHOICES, label=_('Perform Talent'))
    text_talent = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, 
        choices=TEXT_TALENT_CHOICES, label=_('Text Talent'))
    language_talent = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, 
        choices=LANGUAGE_TALENT_CHOICES, label=_('Language Talent'))
    else_talent = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, 
        choices=ELSE_TALENT_CHOICES, label=_('Else Talent'))
    #err...
    custom_music_talent = forms.CharField(required=False, widget=forms.TextInput(attrs={'size':8}), 
        max_length=30, label=_('custom_music_talent'))
    custom_video_talent = forms.CharField(required=False, widget=forms.TextInput(attrs={'size':8}), 
        max_length=30, label=_('custom_video_talent'))
    custom_design_talent = forms.CharField(required=False, widget=forms.TextInput(attrs={'size':8}), 
        max_length=30, label=_('custom_design_talent'))
    custom_art_talent = forms.CharField(required=False, widget=forms.TextInput(attrs={'size':8}), 
        max_length=30, label=_('custom_art_talent'))
    custom_dance_talent = forms.CharField(required=False, widget=forms.TextInput(attrs={'size':8}), 
        max_length=30, label=_('custom_dance_talent'))
    custom_perform_talent = forms.CharField(required=False, widget=forms.TextInput(attrs={'size':8}), 
        max_length=30, label=_('custom_perform_talent'))
    custom_text_talent = forms.CharField(required=False, widget=forms.TextInput(attrs={'size':8}), 
        max_length=30, label=_('custom_text_talent'))
    custom_language_talent = forms.CharField(required=False, widget=forms.TextInput(attrs={'size':8}), 
        max_length=30, label=_('custom_language_talent'))
    custom_else_talent = forms.CharField(required=False, widget=forms.TextInput(attrs={'size':8}), 
        max_length=30, label=_('custom_else_talent'))

    class Meta:
        exclude = ('user', )
        model = UserTalent

class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label=_('New email'))
    emailconf = forms.EmailField(label=_('Confirm email'))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            if User.objects.filter(email=email):
                raise forms.ValidationError(_('this email address has been used.'))
        except User.DoesNotExist:
            pass

        return email

    def clean_emailconf(self):
        email = self.cleaned_data.get('email')
        emailconf = self.cleaned_data.get('emailconf')

        if not email:
            return self.cleaned_data['emailconf']
        
        if email != emailconf:
            raise forms.ValidationError(_('verify email field is different from email feld'))
        return self.cleaned_data['emailconf']

class ForgotPasswordForm(forms.Form):
    TYPE_CHOICES = (
        ('username', _('username')),
        ('email', _('email')),
    )
    type = forms.ChoiceField(choices=TYPE_CHOICES)
    if settings.SITE_ID == 3:
        value = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'input-xxlarge'}))
    else:
        value = forms.CharField(max_length=255)


class NewsPaperForm(forms.ModelForm):
    class Meta:
        model = NewsPaper
        exclude = ('user', )

class InviteFriendsForm(forms.Form):
    invite_emails = forms.CharField(label=_('Invite your friends to join StreetVoice and get your extra web space!'), 
        required=False)

class FacebookRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-xxlarge'}))
    nickname = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-xxlarge'}))
    confirm = forms.BooleanField(required=True)

    def clean_username(self):
        # 限制使用者帳號格式
        if not re.match('^[a-zA-Z]{1}[a-zA-Z0-9_]{2,15}$', self.cleaned_data['username']):
            raise forms.ValidationError(_('username can only contain english, numbers and underscore. \
                Begin with character only.'))

        # 檢查是否已經有帳號存在
        elif User.objects.filter(username__iexact=self.cleaned_data['username']):
            raise forms.ValidationError(_('this username has been registered'))

        if self.cleaned_data['username'] in RESERVED_KEYWORD:
            raise forms.ValidationError(_('this username is not allowed'))

        return self.cleaned_data['username']

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']

        nickname_exists = UserProfile.objects.filter(nickname=nickname).exists()
        if nickname_exists:
            raise forms.ValidationError(_('this nickname has been used'))

        return nickname

class FacebookBindingForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'rel': _('Account'), 'class': 'input-xlarge', 'placeholder': _('Account')}))
    password = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'rel': _('Password'), 'class': 'input-xlarge', 'placeholder': _('Password')}))
    import_picture = forms.BooleanField(required=False)
    
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

class SinaweiboRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'size': 30}))
    email = forms.EmailField(label=_('email'))
    nickname = forms.CharField(widget=forms.TextInput(attrs={'size': 30}))
    birthday = YearMonthDayField(label=_('birthday'), widget=YearMonthDayWidget)
    show_birthday = forms.BooleanField(initial=True, required=False)
    confirm = forms.BooleanField(required=True)

    def clean_username(self):
        username = self.cleaned_data['username']

        # 限制使用者帳號格式
        import re
        if not re.match('^[a-zA-Z]{1}[a-zA-Z0-9_]{2,15}$', username):
            raise forms.ValidationError(_('username can only contain english, numbers and underscore. \
                Begin with character only.'))

        try:
            User.objects.get(username=username)
            raise forms.ValidationError(_('this username has been registered'))
        except User.DoesNotExist:
            pass

        return username

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']

        nickname_exists = UserProfile.objects.filter(nickname=nickname).exists()
        if nickname_exists:
            raise forms.ValidationError(_('this nickname has been used'))

        return nickname    

    def clean_email(self):
        # 檢查是否已有相同 email
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_('This email address is already in use. Please supply another email address.'))
        elif UserTemp.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already registered and waiting for activate. \
                Please activate directly and doesn't need to register again."))
        elif EmailTemp.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is waiting for verifying."))
        return self.cleaned_data['email']


class SinaweiboBindingForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'rel': _('Account')}))
    password = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'rel': _('Password')}))
    import_picture = forms.BooleanField(required=False)

    def clean_username(self):
        if not re.match('^[a-zA-Z]{1}[a-zA-Z0-9_]{2,15}$', self.cleaned_data['username']):
            raise forms.ValidationError(_('username can only contain english, numbers and underscore. \
                Begin with character only.'))

        if self.cleaned_data['username'] in RESERVED_KEYWORD:
            raise forms.ValidationError(_('this username is not allowed'))

        return self.cleaned_data['username']

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


# HK form
class HKProfileForm(forms.Form):
    #accounttype = forms.ChoiceField(label=_('account type'), choices=ACCOUNT_TYPE_CHOICES, widget=forms.RadioSelect)
    avatar = forms.ImageField(required=False, label=_('avatar'), help_text=_('Limited to less than 1MB JPG or GIF files.'), widget=forms.FileInput(attrs={'class': 'input-file'}))
    new_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'size':30, 'class': 'input-xxlarge'}), label=_('Password'), help_text=_('3-12 characters or numbers. First word must be a word.'))
    new_passconf = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'size':30, 'class': 'input-xxlarge'}), label=_('Confirm'), help_text=_('Please enter password again'))
    #email = forms.EmailField(label=_('email'), help_text=_('Recommend you to use the ISP provided or paid mailboxes'),
    #    widget=forms.TextInput(attrs={'size':80, 'class': 'input-xxlarge'}))
    realname = forms.CharField(required=False, max_length=30, label=_('Real name'), widget=forms.TextInput(attrs={'class': 'input-xxlarge'}))
    nickname = forms.CharField(max_length=20, label=_('display name'), widget=forms.TextInput(attrs={'size':30, 'class': 'input-xxlarge'}),
        help_text=_('Please enter the name you want to display, the name is the only'))
    habitat = forms.ChoiceField(choices=HKUSE_HABITAT_CHOICES, label=_('habitat'))
    city = forms.CharField(label=_('city'), required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'input-medium', 'placeholder': _('city')}))
    address = forms.CharField(required=False, max_length=255, label=_('Address'), 
        widget=forms.TextInput(attrs={'size':80, 'class': 'input-xxlarge'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect, label=_('Gender'))
    no_show_age = forms.BooleanField(label=_('do not show age'), required=False)
    self_intro = forms.CharField(widget=forms.Textarea(attrs={'class': 'input-xxlarge', 'rows': 5}), max_length=1000,
        required=False, label=_('Introduction'))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(HKProfileForm, self).__init__(*args, **kwargs)

        year = datetime.datetime.today().year
        BIRTH_YEAR_CHOICES = range(year - 80, year + 1)
        settings.DATE_FORMAT = 'Y n j'
        #birthday_field = YearMonthDayField(label=_('birthday'), widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES))
        birthday_field = forms.DateField(label=_('birthday'), widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES))
        self.fields['birthday'] = birthday_field

    def clean(self):
        cleaned_data = self.cleaned_data

        return cleaned_data

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        if avatar:
            if avatar.size > 1048576:
                raise forms.ValidationError(('Limited to less than 1MB'))

            try:
                ex_name = unicode(avatar.name).rsplit('.', 1)[1]
                if ex_name.lower() not in ('jpg', 'gif', 'png', 'jpeg'):
                    raise forms.ValidationError(_('Please upload correct file format, JPEG or GIF'))
            except IndexError:
                raise forms.ValidationError(_('Please upload correct file format, JPEG or GIF'))

        return avatar

    def clean_new_password(self):
        # 限制密碼格式
        newpwd = self.cleaned_data['new_password']
        if newpwd > '':
            if not re.match('\S{3,12}', newpwd):
                raise forms.ValidationError(_('this password is not valid'))

        return newpwd

    def clean_new_passconf(self):
        newpwd = self.cleaned_data.get('new_password', None)
        newpwdf = self.cleaned_data.get('new_passconf', None)

        if newpwd or newpwdf:
            if newpwd != newpwdf:
                raise forms.ValidationError(_('Password confirm not equal to password'))

        return newpwdf


class HKGroupMemberForm(forms.Form):
    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'input-medium', 'placeholder': _('nick name')}))
    position = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': 'input-large', 'placeholder': _('job title')}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'input-file'}))

    def clean_image(self):
        image = self.cleaned_data['image']

        if image:
            if image.size > 1048576:
                raise forms.ValidationError(('Limited to less than 1MB'))

            try:
                ex_name = unicode(image.name).rsplit('.', 1)[1]
                if ex_name.lower() not in ('jpg', 'gif', 'png', 'jpeg'):
                    raise forms.ValidationError(_('Please upload correct file format, JPEG or GIF'))
            except IndexError:
                raise forms.ValidationError(_('Please upload correct file format, JPEG or GIF'))

        return image


class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        exclude = ('user', )


class HKChangeEmailForm(forms.Form):
    email = forms.EmailField(label=_('New email'), widget=forms.TextInput(attrs={'class': 'input-xxlarge input-noenter'}))
    emailconf = forms.EmailField(label=_('Confirm email'), widget=forms.TextInput(attrs={'class': 'input-xxlarge input-noenter'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            if User.objects.filter(email=email):
                raise forms.ValidationError(_('this email address has been used.'))
        except User.DoesNotExist:
            pass

        return email

    def clean_emailconf(self):
        email = self.cleaned_data.get('email')
        emailconf = self.cleaned_data.get('emailconf')

        if not email:
            return self.cleaned_data['emailconf']
        
        if email != emailconf:
            raise forms.ValidationError(_('verify email field is different from email feld'))
        return self.cleaned_data['emailconf']


class NEWRegisterForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=20, label=_('Username'))
    password = forms.CharField(widget=forms.PasswordInput, label=_('Password'))
    passconf = forms.CharField(widget=forms.PasswordInput, label=_('confirm password'))
    email = forms.EmailField(label=_('email'))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect, label=_('gender'))
    nickname = forms.CharField(max_length=100, label=_('nick name'))
    birthday = YearMonthDayField(label=_('birthday'), widget=YearMonthDayWidget)
    habitat = forms.ChoiceField(choices=HABITAT_CHOICES, label=_('habitat'), required=True)
    city = forms.CharField(label=_('city'), required=False, max_length=50, widget=forms.TextInput())
    address = forms.CharField(required=False, max_length=255, label=_('Address'), widget=forms.TextInput())
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs={'required': True}), label=_('Terms of service'))
    captcha_code = CaptchaField(label=_('captcha code'))

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

        # 檢查待驗證帳號是否已經存在
        if UserTemp.objects.filter(username=self.cleaned_data['username']):
            raise forms.ValidationError(_('this username has been registered and waiting for activate'))

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
                raise forms.ValidationError('Password confirm not equal to password')

        return self.cleaned_data['passconf']

    def clean_nickname(self):
        # 檢查是否已有相同暱稱
        try:
            if UserProfile.objects.filter(nickname=self.cleaned_data['nickname']):
                raise forms.ValidationError(_('this nickname has been used'))
        except UserProfile.DoesNotExist:
            pass

        return self.cleaned_data['nickname']

    def clean_email(self):
        # 檢查是否已有相同 email
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_('This email address is already in use. Please supply another email address.'))
        elif UserTemp.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already registered and waiting for activate. \
                Please activate directly and doesn't need to register again."))
        elif EmailTemp.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is waiting for verifying."))
        return self.cleaned_data['email']


