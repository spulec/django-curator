from django.contrib import admin

from curator.forms import DashboardWidgetForm
from curator.models import Dashboard, DashboardWidget


class DashboardWidgetAdmin(admin.ModelAdmin):
    form = DashboardWidgetForm
    list_display = ('model', 'datetime_field', 'dashboard',)
    
admin.site.register(Dashboard)
admin.site.register(DashboardWidget, DashboardWidgetAdmin)
