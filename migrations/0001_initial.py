# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Dashboard'
        db.create_table('curator_dashboard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('curator', ['Dashboard'])

        # Adding model 'DashboardWidget'
        db.create_table('curator_dashboardwidget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dashboard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['curator.Dashboard'])),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('filter_dict', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('time_period', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('datetime_field', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')(default=200)),
            ('width', self.gf('django.db.models.fields.IntegerField')(default=400)),
        ))
        db.send_create_signal('curator', ['DashboardWidget'])


    def backwards(self, orm):
        
        # Deleting model 'Dashboard'
        db.delete_table('curator_dashboard')

        # Deleting model 'DashboardWidget'
        db.delete_table('curator_dashboardwidget')


    models = {
        'curator.dashboard': {
            'Meta': {'object_name': 'Dashboard'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'curator.dashboardwidget': {
            'Meta': {'object_name': 'DashboardWidget'},
            'dashboard': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['curator.Dashboard']"}),
            'datetime_field': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'filter_dict': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'default': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'time_period': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '400'})
        }
    }

    complete_apps = ['curator']
