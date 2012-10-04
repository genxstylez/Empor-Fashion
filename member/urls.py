from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('member.views',
    url(r'^login/$',        'login',        name='member-login'),
    url(r'^logout/$',       'logout',       name='member-logout'),
    url(r'^register/$',     'register',     name='member-register'),
    url(r'^register/complete$',     'register_complete',     name='member-register-complete'),
    url(r'^activate/(?P<activation_code>\w+)/$',         'activate',        name='member-activate'),

    url(r'facebook/verify/', 'facebook_verify', name='member-facebook-verify'),
    url(r'facebook/connect/done/', 'facebook_connect_done', name='member-facebook-connect-done'),
    url(r'facebook/connect/new/', 'facebook_connect_new', name='member-facebook-connect-new'),
    url(r'facebook/connect/exist/', 'facebook_connect_exist', name='member-facebook-connect-exist'),
    url(r'facebook/connect/', 'facebook_connect', name='member-facebook-connect'),
    url(r'facebook/unbind/', 'facebook_unbind', name='member-facebook-unbind'),
)

