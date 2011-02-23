from django.shortcuts import get_object_or_404, render_to_response

from dashboard.models import Dashboard, DashboardWidget

def dashboard(request, dashboard_name):
    dashboard = get_object_or_404(Dashboard, name=dashboard_name)
    widgets = DashboardWidget.objects.filter(dashboard=dashboard)
    return render_to_response("dashboard/dashboard.html", {
        "dashboard_name": dashboard.name,
        "widgets": widgets,
    })


def widget(request, widget_id):
    widget = get_object_or_404(DashboardWidget, id=widget_id)
    return render_to_response("dashboard/widget.html", {
        "widget": widget,
    })


