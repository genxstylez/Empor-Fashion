from django.shortcuts import redirect
from django.core.urlresolvers import reverse

def index(request):
    if request.user.is_authenticated():
        return redirect(reverse('member-profile', args=[request.user.username]))
    else:
        return redirect(reverse('userena_signin'))
