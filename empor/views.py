# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from empor.models import KeyImpression, Impression

def index(request):
   key = KeyImpression.objects.get(active=True) 
   impressions = Impression.objects.filter(active=True)

   return render(request, 'empor/index.html', {'key': key, 'impressions': impressions})

def test(request):
    return HttpResponse(request.get_host())
