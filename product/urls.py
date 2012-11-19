from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('product.views',
    url(r'^brands/$', 'brands', name='brands'),
    url(r'^brands/(?P<brand_slug>[-\w]+)/$', 'brand', name='brand-view'),
    url(r'^_check_stock/$', '_check_stock', name='product-check-stock'),
    url(r'^(?P<gender_type>MEN|WOMEN)/$', 'gender_products', name='gender-products'),
    url(r'^(?P<gender_type>MEN|WOMEN)/(?P<category>\d+)/$', 'gender_products', name='gender-products-category'),
    url(r'^(?P<brand_slug>[-\w]+)/$', 'brand_products', name='brand-products'),
    url(r'^(?P<brand_slug>[-\w]+)/(?P<gender_type>MEN|WOMEN)/$', 'brand_products', name='brand-products-gender'),
    url(r'^(?P<brand_slug>[-\w]+)/(?P<gender_type>MEN|WOMEN)/(?P<category>\d+)/$', 'brand_products', name='brand-products-gender-category'),
    url(r'^(?P<brand_slug>[-\w]+)/(?P<gender_type>MEN|WOMEN)/(?P<product_slug>[-\w]+)/$', 'product_view', name='product-view'),
    url(r'^(?P<brand_slug>[-\w]+)/(?P<gender_type>MEN|WOMEN)/(?P<category>\d+)/(?P<product_slug>[-\w]+)/$', 'product_view', name='products-view-category'),
)
