from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('order.views',
    url(r'^$', 'index', name='order-index'),
    url(r'shipping/(?P<country_id>\d+)/$', 'get_shipping', name='order-shipping'),
    url(r'my-orders/$', 'orders', name='order-orders'),
    url(r'my-orders/(?P<order_id>\d+)/$', 'info', name='order-info'),
    url(r'paypal/$', 'paypal', name='order-paypal'),
    url(r'success/$', 'success', name='order-success'),
    url(r'thankyou/$', 'thankyou', name='order-thankyou'),
    url(r'voucher-check/$', 'voucher_check', name='order-voucher-check'),
    url(r'voucher-reset/$', 'voucher_reset', name='order-voucher-reset'),
)

