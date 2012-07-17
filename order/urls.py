from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('order.views.site',
    url(r'^$', 'index', name='order-index'),
)

