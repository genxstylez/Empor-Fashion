# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserTemp'
        db.create_table('member_usertemp', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('gender', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('birthday', self.gf('django.db.models.fields.DateField')()),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('country', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('post_code', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('activation_code', self.gf('django.db.models.fields.CharField')(max_length=40, db_index=True)),
            ('tos', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('member', ['UserTemp'])

        # Adding model 'UserProfile'
        db.create_table('member_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('gender', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('birthday', self.gf('django.db.models.fields.DateField')()),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('country', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('post_code', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('reset_code', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('member', ['UserProfile'])

        # Adding model 'FacebookProfile'
        db.create_table('member_facebookprofile', (
            ('uid', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='facebook_profile', unique=True, to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('locale', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('access_token', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('member', ['FacebookProfile'])


    def backwards(self, orm):
        # Deleting model 'UserTemp'
        db.delete_table('member_usertemp')

        # Deleting model 'UserProfile'
        db.delete_table('member_userprofile')

        # Deleting model 'FacebookProfile'
        db.delete_table('member_facebookprofile')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'member.facebookprofile': {
            'Meta': {'object_name': 'FacebookProfile'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'locale': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'uid': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'facebook_profile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'member.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'country': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'post_code': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'reset_code': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'member.usertemp': {
            'Meta': {'object_name': 'UserTemp'},
            'activation_code': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'country': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'post_code': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tos': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['member']