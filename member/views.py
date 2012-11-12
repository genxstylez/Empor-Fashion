# -*- coding: utf-8 -*_
from django.conf import settings
from django.http import Http404, HttpResponse
from django.contrib import auth
from django.utils.translation import ugettext as _
from django.utils.http import urlquote_plus
from django.utils.encoding import iri_to_uri
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.hashcompat import sha_constructor
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.core.mail import EmailMessage
from empor.shortcuts import JsonResponse
from member.models import UserProfile, FacebookProfile, UserTemp
from member.forms import LoginForm, RegisterForm, ReActivateForm, FacebookBindingForm, \
    ChangePasswordForm, ResetPasswordForm, ForgotPasswordForm, ProfileForm
import random
from datetime import datetime

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']

            username = username.lower()

            user_obj = auth.authenticate(username=username, password=password)
            if user_obj:
                auth.login(request, user_obj)

                if remember_me:
                    request.session.set_expiry(0)

                # redirect
                next = request.GET.get('next', None)
                request.flash['message'] = _('Welcome Back!')

                if next and next != 'None':
                    next = iri_to_uri(next)
                    return redirect(next)

                return redirect('index')
            else:
                try:
                    user_temp = UserTemp.objects.get(username=username, password=password)
                    request.session['reactivate_username'] = user_temp.username
                    return reactivate(request)
                except UserTemp.DoesNotExist:
                    next = request.GET.get('next', None)
                    next = urlquote_plus(next)
                    request.flash['message'] = _('Please input correct username / password')
                    if next:
                        return redirect("%s?next=%s" % (reverse('member-login'), next))
                    return login(request)
    else:
        form = LoginForm()
    return render(request, 'member/login.html', {'form':form})

def logout(request):
    auth.logout(request)

    next = request.GET.get('next', None)
    if next:
        next = iri_to_uri(next)
        return redirect(next)
    else:
        return redirect('index')

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            salt = sha_constructor(str(random.random())).hexdigest()[:5]
            activation_code = sha_constructor(salt+data['username']).hexdigest()

            user_temp = form.save(commit=False)
            user_temp.activation_code = activation_code
            user_temp.save()

            html_content = render_to_string('email/activate.html', {
                'host': request.get_host(),
                'STATIC_URL': settings.STATIC_URL,
                'activation_code': activation_code,
                'name': user_temp.first_name,
                'username': user_temp.username,
                'password': user_temp.password
            })

            subject = _('EMPOR Account Activation')

            message = EmailMessage(subject, html_content, settings.DEFAULT_FROM_EMAIL, [user_temp.email])
            message.content_subtype = "html"
            message.send()

            complete_url = "%s?username=%s&email=%s" % \
                (reverse('member-register-complete'), user_temp.username, user_temp.email)
            return redirect(complete_url)
    else:
        form = RegisterForm()
    return render(request, 'member/register.html', {'form': form})

def register_complete(request):
    username = request.GET.get('username')
    email = request.GET.get('email')

    return render(request, 'member/register_complete.html', {'username': username, 'email': email})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        form.save()
    profile = UserProfile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    return render(request, 'member/profile.html', {'form': form})


def activate(request, activation_code):
    user_temp = get_object_or_404(UserTemp, activation_code=activation_code)

    try:
        user = User.objects.get(username=user_temp.username, email=user_temp.email)
    except User.DoesNotExist:
        user = User.objects.create_user(user_temp.username, user_temp.email, user_temp.password)
        user.save()

    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile(
            user = user,
            gender = user_temp.gender,
            phone = user_temp.phone,
            birthday = user_temp.birthday,
            country = user_temp.country,
            post_code = user_temp.post_code,
            address = user_temp.address,
        )
        profile.save()
    user = auth.authenticate(username=user_temp.username, password=user_temp.password)
    if user:
        auth.login(request, user)

    # 刪除認證用的暫存資料 (user temp)
    user_temp.delete()
    url = "%s?username=%s&email=%s" % (reverse('member-reactivate-done'), user.username, user.email)
    return redirect(url)

def activate_done(request):
    return render(request, 'member/activate_done.html')

def reactivate(request):
    ''' 重新發送認證信 '''

    reactivate_username = request.session.get('reactivate_username', None)
    if not reactivate_username:
        raise Http404

    if request.method == 'POST':
        form = ReActivateForm(request.POST)
        if form.is_valid():
            user_temp = User.objects.get(username=reactivate_username)
            user_temp.email = form.cleaned_data['email']
            user_temp.save()

            # 發送註冊信件, 通知啟用
            html_content = render_to_string('member/activate.html', {
                'host': request.get_host(), 
                'activation_code': user_temp.activation_code,
                'username': user_temp.username,
                'password': user_temp.password,
            })

            subject, from_email, to = _('EMPOR activate confirm'), settings.DEFAULT_FROM_EMAIL, user_temp.email

            msg = EmailMessage(subject, html_content, from_email, [to])
            msg.content_subtype = "html"
            msg.send()

            reactivate_complete_url = "%s?username=%s&email=%s" % (reverse('member-reactivate-done'), \
                user_temp.username, user_temp.email)
            return redirect(reactivate_complete_url)
    else:
        form = ReActivateForm(initial={'username': reactivate_username})

    return render(request, 'member/reactivate.html', {'form': form})

def reactivate_done(request):
    ''' 重新認證信件發送成功 '''
    return render(request, 'member/reactivate_done.html') 

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            user = request.user
            user_obj = auth.authenticate(username=user.username, password=old_password)
            if user_obj:
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()
                request.flash['message'] = _('Your password has been changed')
                return redirect('member-profile') 
    form = ChangePasswordForm()
    return render(request, 'member/change_password.html', {'form': form})

def reset_password(request, reset_code):
    try:
        profile = UserProfile.objects.get(reset_code=reset_code)
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                user = profile.user
                new_password = form.cleaned_data['password']
                user.set_password(new_password)
                user.save()
                user_obj = auth.authenticate(username=user.username, password=new_password)
                if user_obj:
                    auth.login(request, user_obj)
                profile.reset_code = ''
                profile.save()
                request.flash['message'] = _('You password has been reset')
                return redirect('member-profile')
        form = ResetPasswordForm()
        return render(request, 'member/change_password.html', {'form': form})
    except UserProfile.DoesNotExist:
        raise Http404
    
def forgot_password(request):
    ''' 忘記密碼 '''

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data['value']

            try:
                if value.find('@') > 0:
                    user = User.objects.get(email=value)
                else:
                    user = User.objects.get(username__iexact=value)
            except User.DoesNotExist:
                request.flash['message']  = _("Can't find this account!")
                return render(request, 'member/forgot_password.html', {'form': form})

            # reset code
            salt = sha_constructor(str(random.random())).hexdigest()[:5]
            reset_code = sha_constructor(salt+user.username).hexdigest()

            html_content = render_to_string('email/reset_password.html', {
                'host': request.get_host(), 
                'STATIC_URL': settings.STATIC_URL,
                'user': user,
                'reset_code': reset_code
            })
            subject = _('EMPOR, Password reset request')

            msg = EmailMessage(subject, html_content, settings.DEFAULT_FROM_EMAIL, [user.email])
            msg.content_subtype = "html"
            msg.send()

            # store reset code
            profile = UserProfile.objects.get(user=user)
            profile.reset_code = reset_code
            profile.save()

            # for display encrypt email address
            email_username, email_domain = str(user.email).split('@')
            encrypt_username = email_username[0] + email_username[1]
            email_username_amount = len(email_username)-2
            while email_username_amount > 0:
                encrypt_username += "*"
                email_username_amount -= 1
            
            return render(request, 'member/forgot_password_sent.html', {
                'form': form,
                'encrypt_username': encrypt_username,
                'email_domain': email_domain,
            })
    form = ForgotPasswordForm()

    return render(request, 'member/forgot_password.html', {'form': form})

#client-side verify
def facebook_verify(request):
    if request.method == 'POST' and request.is_ajax():
        profile = request.POST
        # if user is already connected
        user = auth.authenticate(facebook_uid=profile['id'])
        if user:
            auth.login(request, user)
            return JsonResponse({'success': True})

        request.session['facebook_profile'] = profile

        return JsonResponse({'success': False})
    else:
        raise Http404

def facebook_connect(request):
    profile = request.session.get('facebook_profile', None)
    # for facebook connect 'not agree' user, avoid error
    if not profile:
        return redirect('/')

    email = profile.get('email', None)
    if not email:
        return redirect('/')

    # if user's email already exist
    email_exists = User.objects.filter(email=email).exists()
    if email_exists:
        return redirect('member-facebook-connect-exist')

    return render(request, 'member/facebook/connect.html', {'profile': profile})

def facebook_connect_new(request):
    profile = request.session.get('facebook_profile', None)

    if not profile:
        return redirect('/')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_temp = form.save(commit=False)

            # random password
            password = User.objects.make_random_password()

            # create user
            user = User.objects.create_user(user_temp.username, profile['email'], password)
            user.first_name = user_temp.first_name
            user.last_name = user_temp.last_name
            user.save()

            # user profile
            user_profile = UserProfile(
                user = user,
                gender = user_temp.gender,
                phone = user_temp.phone,
                birthday = user_temp.birthday,
                country = user_temp.country,
                post_code = user_temp.post_code,
                address = user_temp.address,
            )
            user_profile.save()

            # facebook profile
            fbprofile = FacebookProfile(
                uid = profile['id'],
                user = user,
                name = profile.get('name', ''),
                gender = profile.get('gender', 'male'),
                locale = profile['locale'],
                url = profile['link'],
                timezone = profile.get('timezone', ''),
                verified = profile.get('verified', False),
                created_at = datetime.now()
            )
            fbprofile.save()

            # login user
            user = auth.authenticate(username=user.username, password=password)
            auth.login(request, user)

            request.session['fb_connect_type'] = 'new'

            return redirect('member-facebook-connect-done')
    else:
        username = profile.get('username', '')
        birthday = profile.get('birthday', None)
        if birthday:
            birthday = birthday.split('/')
            birthday = birthday[2] + '/' + birthday[1] + '/' + birthday[0]
        gender = profile.get('gender', 0)
        first_name = profile.get('first_name', '')
        last_name = profile.get('last_name', '')
        email = profile.get('email', '')

        form = RegisterForm(initial={
            'username': username, 
            'birthday': birthday, 
            'gender': gender,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
        })

    return render(request, 'member/facebook/new.html', {'profile': profile, 'form': form})

def facebook_connect_exist(request):
    profile = request.session.get('facebook_profile', None)

    if not profile:
        return redirect('/')

    if request.method == 'POST':
        form = FacebookBindingForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            # create facebook profile
            fbprofile = FacebookProfile()
            fbprofile.uid = profile['id']
            fbprofile.user = user
            fbprofile.name = profile['name']
            fbprofile.gender = profile.get('gender', 'male')
            fbprofile.locale = profile['locale']
            fbprofile.url = profile['link']
            fbprofile.timezone = profile.get('timezone', '')
            fbprofile.verified = profile.get('verified', False)
            fbprofile.created_at = datetime.now()
            fbprofile.save()

            if user:
                auth.login(request, user)

            request.session['fb_connect_type'] = 'exist'
            return redirect('member-facebook-connect-done')
    else:
        form = FacebookBindingForm()

    return render(request, 'member/facebook/exist.html', {'form': form, 'profile': profile})

@login_required
def facebook_connect_done(request):
    fb_connect_type = request.session.get('fb_connect_type')

    return render(request, 'member/facebook/done.html', {
        'fb_connect_type': fb_connect_type
    })

@login_required
def facebook_unbind(request):
    try:
        request.user.facebook_profile.delete()
    except FacebookProfile.DoesNotExist:
        pass

    return HttpResponse('done')

 
