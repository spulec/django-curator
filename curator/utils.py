def get_class(class_name):
    parts = class_name.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def get_datetime_fields(class_name):
    class_module = get_class(class_name)
    fields = class_module()._meta.local_fields
    return [(field.name, field.name) for field in fields if field.__class__.__name__ in ['DateField', 'DateTimeField']]
