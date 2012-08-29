from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('order.views',
    url(r'^$', 'index', name='order-index'),
    url(r'my_orders/$', 'orders', name='order-orders'),
    url(r'my_orders/(?P<order_id>\d+)/$', 'info', name='order-info'),
    url(r'paypal/$', 'paypal', name='order-paypal'),
    url(r'success/$', 'success', name='order-success'),
)

