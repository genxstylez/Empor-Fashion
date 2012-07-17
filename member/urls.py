from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('member.views',
    url(r'^$', 'index', name='member-index'),
)
