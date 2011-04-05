import simplejson as json

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response

from curator.models import Dashboard, DashboardWidget
from curator.utils import get_datetime_fields

@staff_member_required
def dashboard(request, dashboard_name):
    dashboard = get_object_or_404(Dashboard, name=dashboard_name)
    widgets = DashboardWidget.objects.filter(dashboard=dashboard).order_by('order')
    return render_to_response("curator/dashboard.html", {
        "dashboard": dashboard,
        "widgets": widgets,
    })

@staff_member_required
def widget(request, widget_id):
    widget = get_object_or_404(DashboardWidget, id=widget_id)
    return render_to_response("curator/widget.html", {
        "widget": widget,
    })

@staff_member_required
def widget_order(request, dashboard_name):
    order_ids = request.POST.get("ids", "")
    ids = order_ids.split(",")
    for index, curr_id in enumerate(ids):
        widget = DashboardWidget.objects.get(id=curr_id)
        widget.order = index
        widget.save()
    return HttpResponse("ok")

@staff_member_required
def widget_size(request):
    widget_id = request.POST.get("id")
    height = int(round(float(request.POST.get("height"))))
    width = int(round(float(request.POST.get("width"))))
    widget = DashboardWidget.objects.get(id=widget_id)
    widget.height = height
    widget.width = width
    widget.save()
    return HttpResponse("ok")

@staff_member_required
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

@staff_member_required
def model_fields(request, model_name):
    fields = get_datetime_fields(model_name)
    return HttpResponse(json.dumps(fields), mimetype='application/json')
    

