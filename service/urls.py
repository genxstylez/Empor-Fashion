# -*- coding: utf-8 -*_
from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('service.views',
    url(r'^$', 'index', name='service-index'),
    url(r'faq/$', 'faq', name='service-faq'),
)
