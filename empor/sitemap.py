from django.core.urlresolvers import reverse
from django.contrib.sitemaps import GenericSitemap, Sitemap
from product.models import Product

class ViewSitemap(Sitemap):
    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)

product = {'queryset': Product.on_site.all(), 'date_field': 'last_modified'}
sitemaps = {
    'views': ViewSitemap,
    'products': GenericSitemap(product, priority=0.9, changefreq='daily'),
}
