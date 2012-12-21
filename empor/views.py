# -*- coding: utf-8 -*-
from django.shortcuts import render
from empor.models import KeyImpression, Impression

def index(request):
    
    key = KeyImpression.objects.filter(active=True) 
    key = key[0] if key else None

    impressions = Impression.objects.filter(active=True)

    return render(request, 'empor/index.html', {'key': key, 'impressions': impressions})
