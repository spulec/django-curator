# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Dashboard'
        db.create_table('dashboard_dashboard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('dashboard', ['Dashboard'])

        # Adding model 'DashboardWidget'
        db.create_table('dashboard_dashboardwidget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dashboard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Dashboard'])),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('filter_dict', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('time_period', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('date_field', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('dashboard', ['DashboardWidget'])


    def backwards(self, orm):
        
        # Deleting model 'Dashboard'
        db.delete_table('dashboard_dashboard')

        # Deleting model 'DashboardWidget'
        db.delete_table('dashboard_dashboardwidget')


    models = {
        'dashboard.dashboard': {
            'Meta': {'object_name': 'Dashboard'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'dashboard.dashboardwidget': {
            'Meta': {'object_name': 'DashboardWidget'},
            'dashboard': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dashboard.Dashboard']"}),
            'date_field': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'filter_dict': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'time_period': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['dashboard']
