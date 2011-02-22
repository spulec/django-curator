# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'DashboardWidget.date_field'
        db.delete_column('dashboard_dashboardwidget', 'date_field')

        # Adding field 'DashboardWidget.datetime_field'
        db.add_column('dashboard_dashboardwidget', 'datetime_field', self.gf('django.db.models.fields.CharField')(default='date_joined', max_length=255), keep_default=False)

        # Changing field 'DashboardWidget.filter_dict'
        db.alter_column('dashboard_dashboardwidget', 'filter_dict', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'DashboardWidget.date_field'
        raise RuntimeError("Cannot reverse this migration. 'DashboardWidget.date_field' and its values cannot be restored.")

        # Deleting field 'DashboardWidget.datetime_field'
        db.delete_column('dashboard_dashboardwidget', 'datetime_field')

        # Changing field 'DashboardWidget.filter_dict'
        db.alter_column('dashboard_dashboardwidget', 'filter_dict', self.gf('django.db.models.fields.CharField')(default='', max_length=255))


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'time_period': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['dashboard']
