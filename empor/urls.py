from django.conf.urls import patterns, include, url
from empor import settings
from django.contrib import admin
from member.forms import RegisterForm
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'empor.views.index', name='index'),
    url(r'^empor/', include('product.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
    (r'^accounts/signup/$','userena.views.signup', {'signup_form': RegisterForm}),
    (r'^accounts/', include('userena.urls')),
    
)

