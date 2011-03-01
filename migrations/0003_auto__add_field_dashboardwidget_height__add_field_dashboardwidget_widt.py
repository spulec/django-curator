# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'DashboardWidget.height'
        db.add_column('dashboard_dashboardwidget', 'height', self.gf('django.db.models.fields.IntegerField')(default=500), keep_default=False)

        # Adding field 'DashboardWidget.width'
        db.add_column('dashboard_dashboardwidget', 'width', self.gf('django.db.models.fields.IntegerField')(default=700), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'DashboardWidget.height'
        db.delete_column('dashboard_dashboardwidget', 'height')

        # Deleting field 'DashboardWidget.width'
        db.delete_column('dashboard_dashboardwidget', 'width')


    models = {
        'dashboard.dashboard': {
            'Meta': {'object_name': 'Dashboard'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'dashboard.dashboardwidget': {
            'Meta': {'object_name': 'DashboardWidget'},
            'dashboard': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dashboard.Dashboard']"}),
            'datetime_field': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'filter_dict': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'time_period': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['dashboard']
