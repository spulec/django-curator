import ast

from django.db import models

def get_model_choices():
    apps = [app for app in models.get_apps()]
    all_models = []
    for app in apps:
        all_models += models.get_models(app)
    return [(model.__module__ + "." + model.__name__, model.__module__ + "." + model.__name__) for model in all_models]

MODEL_CHOICES = get_model_choices()
TIME_PERIOD_CHOICES = (
    ('DA', 'Daily'),
    ('WE', 'Weekly'),
    ('MO', 'Monthly'),
)


class Dashboard(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class DashboardWidget(models.Model):
    dashboard = models.ForeignKey(Dashboard)
    model = models.CharField(max_length=255, choices=MODEL_CHOICES)
    filter_dict = models.CharField(max_length=255, blank=True, null=True)
    time_period = models.CharField(max_length=2, choices=TIME_PERIOD_CHOICES)
    datetime_field = models.CharField(max_length=255)
    order = models.IntegerField()

    def __unicode__(self):
        return "%s : %s" % (self.dashboard, self.model)

    def get_class(self, kls):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)            
        return m
       
    def get_date_filter(self):
       return {}
       #TODO finish this
       """
       if self.time_period == 'DA':
           date_filter[ 
       elif self.time_period == 'WE':
           date_filter = 
       elif self.time_period == 'MO':
           date_filter = 
       """   

    def data_points(self):
       filter_dict_mapped = ast.literal_eval(self.filter_dict) if self.filter_dict else {}
       date_filter = self.get_date_filter()
       # Merge the dicts
       overall_filter = dict(filter_dict_mapped, **date_filter)
       return self.get_class(self.model).objects.filter(**overall_filter).order_by(self.datetime_field)

    def data_list(self):
        data_array = []
        #TODO determine point/minute or whatever
        for index, data_point in enumerate(self.data_points()):
            datetime = getattr(data_point, self.datetime_field)
            data_array.append([datetime, index + 1])
        return data_array


