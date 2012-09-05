from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('staff.views',
    url(r'^$',                                          'index',                name='staff-index'),
    url(r'^collection/(?P<collection_id>\d+)/$',                               'collection',           name='staff-collection'),
    url(r'^collection/create/$',                                   'collection_create',    name='staff-create-collection'),
    url(r'^collection/(?P<collection_id>\d+)/product/create/$',    'product_create',       name='staff-create-product'),
    url(r'^collection/(?P<collection_id>\d+)/product/edit/(?P<product_id>\d+)/$',    'product_edit',       name='staff-edit-product'),
    url(r'^product/(?P<product_id>\d+)/image/$',        'product_image',       name='staff-product-image'),
    url(r'^product/(?P<product_id>\d+)/thumbnail/$',    'product_thumb',       name='staff-product-thumb'),

    url(r'^render_options/(?P<group_id>\d+)/$', '_render_options',      name='staff-render-options'),
    url(r'^_upload/$',                          '_upload',              name='staff-upload'),
    url(r'^_thumb_upload/$',                    '_thumb_upload',        name='staff-thumb-upload'),
    url(r'^create/category$',                   '_create_category',     name='staff-create-category'),
    url(r'^create/brand$',                      '_create_brand',        name='staff-create-brand'),
    url(r'^create/option_group$',               '_create_optiongroup',  name='staff-create-optiongroup'),
)
