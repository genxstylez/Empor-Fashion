from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('vote.views',
    url(r'^$', 'vote', name='vote'),
)
