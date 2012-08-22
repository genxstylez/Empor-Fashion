from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('product.views.site',
    url(r'^(?P<brand>\w+)/(?P<product_slug>\w+)/$', 'product_view', name='product-view'),
)
