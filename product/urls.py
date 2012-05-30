from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('product.views.admin',
    url(r'^admin/$', 'index', name='product-admin-index'),
    url(r'^admin/create/$', 'create', name='product-admin-create'),
)
