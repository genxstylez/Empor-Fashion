# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Product.discount'
        db.add_column('product_product', 'discount',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='products', null=True, to=orm['discount.Discount']),
                      keep_default=False)


        # Changing field 'ProductThumb.thumb'
        db.alter_column('product_productthumb', 'thumb', self.gf('django.db.models.fields.files.ImageField')(max_length=255))

        # Changing field 'ProductThumb.original'
        db.alter_column('product_productthumb', 'original', self.gf('django.db.models.fields.files.ImageField')(max_length=255))

    def backwards(self, orm):
        # Deleting field 'Product.discount'
        db.delete_column('product_product', 'discount_id')


        # Changing field 'ProductThumb.thumb'
        db.alter_column('product_productthumb', 'thumb', self.gf('django.db.models.fields.files.ImageField')(max_length=100))

        # Changing field 'ProductThumb.original'
        db.alter_column('product_productthumb', 'original', self.gf('django.db.models.fields.files.ImageField')(max_length=100))

    models = {
        'discount.discount': {
            'Meta': {'object_name': 'Discount'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'allowUses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'numUses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'percentage': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'product.brand': {
            'Meta': {'object_name': 'Brand'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'brands'", 'symmetrical': 'False', 'to': "orm['product.Category']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'story': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'w_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        'product.category': {
            'Meta': {'object_name': 'Category'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'categories'", 'symmetrical': 'False', 'to': "orm['product.Gender']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['product.Category']"})
        },
        'product.collection': {
            'Meta': {'object_name': 'Collection'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product.Brand']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gender': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['product.Gender']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'stock': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'product.gender': {
            'Meta': {'object_name': 'Gender'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'product.option': {
            'Meta': {'object_name': 'Option'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'option_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'options'", 'to': "orm['product.OptionGroup']"})
        },
        'product.optiongroup': {
            'Meta': {'object_name': 'OptionGroup'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'product.product': {
            'Meta': {'unique_together': "(('slug', 'brand', 'option'),)", 'object_name': 'Product'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': "orm['product.Brand']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': "orm['product.Category']"}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': "orm['product.Collection']"}),
            'composition': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'discount': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'to': "orm['discount.Discount']"}),
            'discountable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gender': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'products'", 'symmetrical': 'False', 'to': "orm['product.Gender']"}),
            'has_options': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'to': "orm['product.Option']"}),
            'option_group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'to': "orm['product.OptionGroup']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['product.Product']"}),
            'price': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'sold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'stock': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'product.productimage': {
            'Meta': {'object_name': 'ProductImage'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'large_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'large_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'medium_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'medium_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['product.Product']"}),
            'small_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'small_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        'product.productthumb': {
            'Meta': {'object_name': 'ProductThumb'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'product': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'thumb'", 'unique': 'True', 'null': 'True', 'to': "orm['product.Product']"}),
            'thumb': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'x1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'x2': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y2': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'product.sizeconversion': {
            'Meta': {'object_name': 'SizeConversion'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product.Brand']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['product']