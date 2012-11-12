# -*- coding: utf-8 -*_
from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('service.views',
    url(r'^$', 'center', name='service-center'),
    url(r'faq/$', 'faq', name='service-faq'),
)
urlpatterns += patterns('',
    url(r'^tos/$', 'django.views.generic.simple.direct_to_template', {'template': 'service/tos.html'}, name='service-tos')
)
