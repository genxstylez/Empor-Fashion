# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import Group
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from service.forms import QuestionForm

@csrf_protect
def center(request):
    spam = request.POST.get('spam', None)
    if spam:
        return HttpResponse('spam')
    if request.user.is_authenticated():
        initial = {'email': request.user.email, 'phone': request.user.profile.phone, 'name': request.user.get_name() }
    else:
        initial = None
    form = QuestionForm(request.POST or None, initial=initial)
    if form.is_valid():
        if request.user.is_authenticated:
            form.save(commit=False)
            form.user = request.user

        question = form.save()
        if question.type == 2:
            group = Group.objects.get(name='Sales').user_set.only('email')
            subject = 'EMPOR 業務- %s' % question.subject.encode('utf-8')
        else:
            group = Group.objects.get(name='Service').user_set.only('email')
            subject = 'EMPOR 客服中心 - %s' % question.subject.encode('utf-8')

        group_email = [ user.email for user in group ]
        send_mail(subject, question.content, question.email, group_email, fail_silently=False)
        request.flash['message'] = _('Your email has been sent!')
        
    return render(request, 'service/center.html', {'form': form})
    
def faq(request):
    return render(request, 'service/faq.html')
