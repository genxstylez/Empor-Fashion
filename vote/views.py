from django.shortcuts import render
from empor.shortcuts import JsonResponse
from vote.models import *

def vote(request):

    if request.POST:
        post_items = request.POST.getlist('items[]', '')
        items = Item.objects.filter(id__in=post_items)
        for item in items:
            item.vote_count += 1
            item.save()
        return JsonResponse({'success': True})

    men_items = Item.objects.filter(category__name='MEN')
    women_items = Item.objects.filter(category__name='WOMEN')
    return render(request, 'vote/index.html', {'men_items': men_items, 'women_items': women_items})
         
