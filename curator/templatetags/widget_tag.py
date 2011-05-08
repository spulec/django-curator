from django import template

register = template.Library()


@register.inclusion_tag("curator/widget_block_head.html")
def widget_tag_head(widget, fullscreen=0):
    #widget_data, time_intervals = widget.data_list()
    return {
            'widget': widget,
            'model_name': widget.get_model_display(),
            'fullscreen': fullscreen,
            #'time_intervals': time_intervals,
            #'data_points': widget_data,
        }


@register.inclusion_tag("curator/widget_block_body.html")
def widget_tag_body(widget):
    return {
            'widget': widget,
        }
