from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('product.views',
    url(r'^(?P<gender_type>MEN|WOMEN)/$', 'products', name='products-view-gender'),
    url(r'^$', 'products', name='products-view'),
    url(r'^(?P<brand_slug>[-\w]+)/(?P<product_slug>[-\w]+)/$', 'product_view', name='product-view'),
)
