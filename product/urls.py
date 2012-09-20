from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('product.views',
    url(r'^(?P<gender_type>MEN|WOMEN)/$', 'products', name='products-view'),
    url(r'^$', 'products', name='products-view'),
    url(r'^(?P<brand>\w+)/(?P<product_slug>\w+)/$', 'product_view', name='product-view'),
)
