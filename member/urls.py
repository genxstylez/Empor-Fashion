from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('member.views',
    url(r'^login/$',        'login',        name='member-login'),
    url(r'^logout/$',       'logout',       name='member-logout'),
    url(r'^register/$',     'register',     name='member-register'),
    url(r'^register/complete/$',                        'register_complete',    name='member-register-complete'),
    url(r'^profile/$',      'profile',     name='member-profile'),
    url(r'^activate/(?P<activation_code>\w+)/$',        'activate',             name='member-activate'),
    url(r'^activate_done/$',                            'activate_done',        name='member-activate-done'),
    url(r'^reactivate/$',                               'reactivate',           name='member-reactivate'),
    url(r'^reactivate_done/$',                          'reactivate_done',      name='member-reactivate-done'),
    url(r'^reset_password/(?P<reset_code>\w+)/$',       'reset_password',       name='member-reset-password'),
    url(r'^forgot_password/$',                          'forgot_password',      name='member-forgot-password'),
    url(r'^change_password/$',                          'change_password',      name='member-change-password'),

    url(r'facebook/verify/', 'facebook_verify', name='member-facebook-verify'),
    url(r'facebook/connect/done/', 'facebook_connect_done', name='member-facebook-connect-done'),
    url(r'facebook/connect/new/', 'facebook_connect_new', name='member-facebook-connect-new'),
    url(r'facebook/connect/exist/', 'facebook_connect_exist', name='member-facebook-connect-exist'),
    url(r'facebook/connect/', 'facebook_connect', name='member-facebook-connect'),
    url(r'facebook/unbind/', 'facebook_unbind', name='member-facebook-unbind'),
)

