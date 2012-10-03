from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('member.views',
    url(r'^login/$',        'login',        name='member-login'),
    url(r'^logout/$',       'logout',       name='member-logout'),
    url(r'^register/$',     'register',     name='member-register'),
    url(r'^register/complete$',     'register_complete',     name='member-register-complete'),
    url(r'^activate/(?P<activation_code>\w+)/$',         'activate',        name='member-activate')
)

