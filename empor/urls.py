from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'empor.views.index', name='index'),
    url(r'^test/$', 'empor.views.test', name='test'),
    url(r'^staff/', include('staff.urls')),
    url(r'^accounts/', include('member.urls')),
    url(r'^products/', include('product.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^discount/', include('discount.urls')),
    url(r'^order/', include('order.urls')),
    url(r'^service/', include('service.urls')),
)
