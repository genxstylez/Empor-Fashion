from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('product.views.admin',
    url(r'^admin/$', 'index', name='product-admin-index'),
    url(r'^admin/render_options/(?P<group_id>\d+)/$', '_render_options', name='product-admin-render-options'),
    url(r'^admin/_upload/$', '_upload', name='product-admin-upload'),
    url(r'^admin/_thumb_upload/$', '_thumb_upload', name='product-admin-upload'),
    url(r'^admin/create/$', 'create_group', name='product-admin-create-group'),
    url(r'^admin/create/(?P<group_id>\d+)/$', 'create_product', name='product-admin-create-product'),
    url(r'^admin/create/category$', '_create_category', name='product-admin-create-category'),
    url(r'^admin/create/brand$', '_create_brand', name='product-admin-create-brand'),
    url(r'^admin/create/option_group$', '_create_optiongroup', name='product-admin-create-optiongroup'),
)

urlpatterns += patterns('product.views.site',
    url(r'^product/(?P<product_id>\d+)/$', 'product_view', name='product-view'),
)
