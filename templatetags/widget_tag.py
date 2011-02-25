from django import template

register = template.Library()

@register.inclusion_tag("dashboard/widget_block_head.html")
def widget_tag_head(widget):
    widget_data = widget.data_list()
    return {
            'widget': widget,
            'model_name': widget.get_model_display(),
            'data_points': widget_data,
        }

@register.inclusion_tag("dashboard/widget_block_body.html")
def widget_tag_body(widget):
    return {
            'widget': widget,
        }

