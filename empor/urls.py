# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from empor.sitemap import sitemaps
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'empor.views.index', name='index'),
    url(r'^staff/', include('staff.urls')),
    url(r'^accounts/', include('member.urls')),
    url(r'^products/', include('product.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^discount/', include('discount.urls')),
    url(r'^order/', include('order.urls')),
    url(r'^service/', include('service.urls')),
    url(r'^vote/', include('vote.urls')),

    (r'^paypal/emporipnreal/', include('paypal.standard.ipn.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)
