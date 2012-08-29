from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('cart.views',
    url(r'^$', 'index', name='cart-index'),
    url(r'^add/$', 'add_item', name='cart-add'),
    url(r'^remove/$', 'remove_item', name='cart-remove'),
)
