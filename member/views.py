# -*- coding: utf-8 -*_
from django.conf import settings
from django.http import HttpResponse
from django.contrib import auth
from django.utils.translation import ugettext as _
from django.utils.http import urlquote_plus
from django.utils.encoding import iri_to_uri
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.hashcompat import sha_constructor
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.core.mail import EmailMessage
from member.models import UserProfile, FacebookProfile, UserTemp
from member.forms import LoginForm, RegisterForm
import random

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

                except User.DoesNotExist:
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

            # 產生認證碼
            salt = sha_constructor(str(random.random())).hexdigest()[:5]
            activation_code = sha_constructor(salt+data['username']).hexdigest()

            user_temp = form.save(commit=False)
            user_temp.activation_code = activation_code
            user_temp.save()

             # 發送註冊信件, 通知啟用
            html_content = render_to_string('email/activate.html', {
                'host': request.get_host(),
                'STATIC_URL': settings.STATIC_URL,
                'activation_code': activation_code,
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
    ''' 帳號申請完成 '''

    username = request.GET.get('username')
    email = request.GET.get('email')

    return render(request, 'member/register_complete.html', {'username': username, 'email': email})

def activate(request, activation_code):
    ''' 帳號啟用頁 '''

    user_temp = get_object_or_404(UserTemp, activation_code=activation_code)

    # 建立使用者
    try:
        user = User.objects.get(username=user_temp.username, email=user_temp.email)
    except User.DoesNotExist:
        user = User.objects.create_user(user_temp.username, user_temp.email, user_temp.password)
        user.save()

    # 建立使用者的會員資料 ( user profile )
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile(
            user = user,
            phone = user_temp.phone,
            billing_recipient = user_temp.billing_recipient,
            billing_street1 = user_temp.billing_street1,
            billing_street2 = user_temp.billing_street2,
            billing_city = user_temp.billing_city,
            billing_post_code = user_temp.billing_post_code,
            billing_country = user_temp.billing_country,
            shipping_recipient = user_temp.shipping_recipient,
            shipping_street1 = user_temp.shipping_street1,
            shipping_street2 = user_temp.shipping_street2,
            shipping_city = user_temp.shipping_city,
            shipping_post_code = user_temp.shipping_post_code,
            shipping_country = user_temp.shipping_country,
            activation_code = activation_code,
        )
        profile.save()
    # 登入使用者
    user = auth.authenticate(username=user_temp.username, password=user_temp.password)
    if user:
        auth.login(request, user)

    # 刪除認證用的暫存資料 (user temp)
    user_temp.delete()

    return activation_done(request)

def activation_done(request):
    return render(request, 'member/activation_done.html')

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

