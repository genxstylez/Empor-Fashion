from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from member.forms import RegisterForm, ProfileForm
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^$', 'empor.views.index', name='index'),
    url(r'^(?P<gender_type>MEN|WOMEN)/$', 'empor.views.gender', name='index-gender'),
    url(r'^staff/', include('staff.urls')),
    url(r'^product/', include('product.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^discount/', include('discount.urls')),
    url(r'^order/', include('order.urls')),
    url(r'^member/', include('member.urls')),
    url(r'^service/', include('service.urls')),
    url(r'^accounts/password/reset/$', auth_views.password_reset, 
        {'template_name': 'userena/password_reset_form.html',
        'email_template_name': 'userena/emails/password_reset_message.txt'},
        name="member-password-reset"),
    (r'^accounts/signup/$','userena.views.signup', {'signup_form': RegisterForm}),
    (r'^accounts/signin/$','userena.views.signin'),
    (r'^accounts/signout/$','userena.views.signout'),
    url(r'^accounts/(?P<username>[\.\w]+)/$','userena.views.profile_edit', {'edit_profile_form': ProfileForm}, name="member-profile"),
    (r'^accounts/', include('userena.urls')),
)
