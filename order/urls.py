from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('order.views.site',
    url(r'^$', 'index', name='order-index'),
    url(r'my_orders/$', 'orders', name='order-orders'),
    url(r'my_orders/(?P<order_id>\d+)/$', 'info', name='order-info'),
    url(r'paypal/(?P<order_id>\d+)/$', 'paypal', name='order-paypal'),
    url(r'success/(?P<order_id>\d+)/$', 'success', name='order-success'),
)

