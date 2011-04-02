import simplejson as json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response

from dashboard.models import Dashboard, DashboardWidget
from dashboard.utils import get_datetime_fields

@login_required
def dashboard(request, dashboard_name):
    dashboard = get_object_or_404(Dashboard, name=dashboard_name)
    widgets = DashboardWidget.objects.filter(dashboard=dashboard).order_by('order')
    return render_to_response("dashboard/dashboard.html", {
        "dashboard": dashboard,
        "widgets": widgets,
    })

@login_required
def widget(request, widget_id):
    widget = get_object_or_404(DashboardWidget, id=widget_id)
    return render_to_response("dashboard/widget.html", {
        "widget": widget,
    })

@login_required
def widget_order(request, dashboard_name):
    order_ids = request.POST.get("ids", "")
    ids = order_ids.split(",")
    for index, curr_id in enumerate(ids):
        widget = DashboardWidget.objects.get(id=curr_id)
        widget.order = index
        widget.save()
    return HttpResponse("ok")

@login_required
def widget_size(request):
    widget_id = request.POST.get("id")
    height = int(round(float(request.POST.get("height"))))
    width = int(round(float(request.POST.get("width"))))
    widget = DashboardWidget.objects.get(id=widget_id)
    widget.height = height
    widget.width = width
    widget.save()
    return HttpResponse("ok")

@login_required
def widget_data(request, widget_id):
    widget = get_object_or_404(DashboardWidget, id=widget_id)
    widget_data, prev_widget_data, time_intervals, prev_time_offset = widget.data_list()
    json_data = {}
    json_data['data_points'] = widget_data
    json_data['prev_data_points'] = prev_widget_data
    json_data['time_intervals'] = time_intervals
    json_data['prev_time_offset'] = prev_time_offset
    json_data['height'] = widget.height
    json_data['width'] = widget.width
    return HttpResponse(json.dumps(json_data), mimetype='application/json')

@login_required
def model_fields(request, model_name):
    fields = get_datetime_fields(model_name)
    return HttpResponse(json.dumps(fields), mimetype='application/json')
    

