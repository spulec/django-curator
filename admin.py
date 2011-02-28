from django.contrib import admin

from dashboard.forms import DashboardWidgetForm
from dashboard.models import Dashboard, DashboardWidget

class DashboardWidgetAdmin(admin.ModelAdmin):
    form = DashboardWidgetForm

admin.site.register(Dashboard)
admin.site.register(DashboardWidget, DashboardWidgetAdmin)
