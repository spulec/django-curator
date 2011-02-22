from django.shortcuts import get_object_or_404, render_to_response

from dashboard.models import DashboardWidget

def widget(request, widget_id):
    widget = get_object_or_404(DashboardWidget, id=widget_id)
    widget_data = widget.data_list()
    return render_to_response("dashboard/widget.html", {
            'data_points': widget_data,
        })
