from django.core.management.base import BaseCommand
from product.models import Product, Collection

class Command(BaseCommand):
    def handle(self, **options):
        collection = Collection.objects.all()
        products = Product.objects.filter(parent=None, collection=collection)
        for i, product in enumerate(products, start=1):
            value = i
            product.sku = product.brand.name[:3].upper() + '%04d%04d' % (product.collection.id , value)
            product.save()
            children = Product.objects.filter(parent=product)
            for child in children:
                child.sku = product.sku + '-%s' % child.option.name
                child.save()

