from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('discount.views',
    url(r'^$', 'index', name='discount-index'),
)
