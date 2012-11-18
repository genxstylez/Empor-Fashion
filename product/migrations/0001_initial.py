# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Gender'
        db.create_table('product_gender', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('product', ['Gender'])

        # Adding model 'Category'
        db.create_table('product_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['product.Category'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('product', ['Category'])

        # Adding M2M table for field gender on 'Category'
        db.create_table('product_category_gender', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm['product.category'], null=False)),
            ('gender', models.ForeignKey(orm['product.gender'], null=False))
        ))
        db.create_unique('product_category_gender', ['category_id', 'gender_id'])

        # Adding model 'Brand'
        db.create_table('product_brand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('w_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('story', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('product', ['Brand'])

        # Adding M2M table for field categories on 'Brand'
        db.create_table('product_brand_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('brand', models.ForeignKey(orm['product.brand'], null=False)),
            ('category', models.ForeignKey(orm['product.category'], null=False))
        ))
        db.create_unique('product_brand_categories', ['brand_id', 'category_id'])

        # Adding model 'Collection'
        db.create_table('product_collection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('stock', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('sold', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['product.Brand'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['product.Category'])),
        ))
        db.send_create_signal('product', ['Collection'])

        # Adding M2M table for field gender on 'Collection'
        db.create_table('product_collection_gender', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('collection', models.ForeignKey(orm['product.collection'], null=False)),
            ('gender', models.ForeignKey(orm['product.gender'], null=False))
        ))
        db.create_unique('product_collection_gender', ['collection_id', 'gender_id'])

        # Adding model 'OptionGroup'
        db.create_table('product_optiongroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('product', ['OptionGroup'])

        # Adding model 'Option'
        db.create_table('product_option', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('option_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='options', to=orm['product.OptionGroup'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('product', ['Option'])

        # Adding model 'Product'
        db.create_table('product_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('sku', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['product.Product'])),
            ('stock', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('sold', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='products', to=orm['product.Category'])),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='products', to=orm['product.Collection'])),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(related_name='products', to=orm['product.Brand'])),
            ('option_group', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='products', null=True, to=orm['product.OptionGroup'])),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='products', null=True, to=orm['product.Option'])),
            ('price', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('composition', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('discountable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_options', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('product', ['Product'])

        # Adding unique constraint on 'Product', fields ['slug', 'brand', 'option']
        db.create_unique('product_product', ['slug', 'brand_id', 'option_id'])

        # Adding M2M table for field gender on 'Product'
        db.create_table('product_product_gender', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['product.product'], null=False)),
            ('gender', models.ForeignKey(orm['product.gender'], null=False))
        ))
        db.create_unique('product_product_gender', ['product_id', 'gender_id'])

        # Adding model 'ProductThumb'
        db.create_table('product_productthumb', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='thumb', unique=True, null=True, to=orm['product.Product'])),
            ('original', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('thumb', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('x1', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('y1', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('x2', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('y2', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('product', ['ProductThumb'])

        # Adding model 'ProductImage'
        db.create_table('product_productimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['product.Product'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('small_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('small_height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('medium_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('medium_height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('large_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('large_height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('main', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('product', ['ProductImage'])


    def backwards(self, orm):
        # Removing unique constraint on 'Product', fields ['slug', 'brand', 'option']
        db.delete_unique('product_product', ['slug', 'brand_id', 'option_id'])

        # Deleting model 'Gender'
        db.delete_table('product_gender')

        # Deleting model 'Category'
        db.delete_table('product_category')

        # Removing M2M table for field gender on 'Category'
        db.delete_table('product_category_gender')

        # Deleting model 'Brand'
        db.delete_table('product_brand')

        # Removing M2M table for field categories on 'Brand'
        db.delete_table('product_brand_categories')

        # Deleting model 'Collection'
        db.delete_table('product_collection')

        # Removing M2M table for field gender on 'Collection'
        db.delete_table('product_collection_gender')

        # Deleting model 'OptionGroup'
        db.delete_table('product_optiongroup')

        # Deleting model 'Option'
        db.delete_table('product_option')

        # Deleting model 'Product'
        db.delete_table('product_product')

        # Removing M2M table for field gender on 'Product'
        db.delete_table('product_product_gender')

        # Deleting model 'ProductThumb'
        db.delete_table('product_productthumb')

        # Deleting model 'ProductImage'
        db.delete_table('product_productimage')


    models = {
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
            'story': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'w_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
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
            'original': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'product': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'thumb'", 'unique': 'True', 'null': 'True', 'to': "orm['product.Product']"}),
            'thumb': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'x1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'x2': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y2': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['product']