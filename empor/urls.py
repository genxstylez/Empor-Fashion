from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from member.forms import RegisterForm, ProfileForm
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
    url(r'^accounts/password/reset/$', auth_views.password_reset, 
        {'template_name': 'userena/password_reset_form.html',
        'email_template_name': 'userena/emails/password_reset_message.txt'},
        name="member-password-reset"),
)
