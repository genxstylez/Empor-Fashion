from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('product.views.staff',
    url(r'^$',                                  'index',                name='staff-index'),
    url(r'^create/$',                           'collection_create',    name='staff-create-collection'),
    url(r'^create/(?P<collection_id>\d+)/product/$', 'product_create',       name='staff-create-product'),

    url(r'^render_options/(?P<group_id>\d+)/$', '_render_options',      name='staff-render-options'),
    url(r'^_upload/$',                          '_upload',              name='staff-upload'),
    url(r'^_thumb_upload/$',                    '_thumb_upload',        name='staff-thumb-upload'),
    url(r'^create/category$',                   '_create_category',     name='staff-create-category'),
    url(r'^create/brand$',                      '_create_brand',        name='staff-create-brand'),
    url(r'^create/option_group$',               '_create_optiongroup',  name='staff-create-optiongroup'),
)
