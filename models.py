import ast
import datetime

from django.db import models

def get_model_choices():
    apps = [app for app in models.get_apps()]
    all_models = []
    for app in apps:
        all_models += models.get_models(app)
    return [(model.__module__ + "." + model.__name__, model.__name__) for model in all_models]

MODEL_CHOICES = get_model_choices()
TIME_PERIOD_CHOICES = (
    ('DA', 'Daily'),
    ('WE', 'Weekly'),
    #('MO', 'Monthly'),
    # TODO add more
)

LOADING_IMG_HEIGHT = 19
LOADING_IMG_WIDTH = 220

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
    height = models.IntegerField()
    width = models.IntegerField()

    def __unicode__(self):
        return "%s : %s" % (self.dashboard, self.model)

    def get_class(self):
        kls = self.model
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)            
        return m
    
    def get_datetime_fields(self):
        fields = self.get_class()._meta.local_fields
        return [(field.name, field.name) for field in fields if field.__class__.__name__ in ['DateField', 'DateTimeField']]

    def get_time_edges(self):
        now = datetime.datetime.now()
        today = datetime.date.today()

        if self.time_period == 'DA':
             return (today, now)
        elif self.time_period == 'WE':
             return (today - datetime.timedelta(days=7), now)
        #return (None, None)

    def data_points(self):
        filter_dict_mapped = ast.literal_eval(self.filter_dict) if self.filter_dict else {}
        date_query = str("%s__range" % self.datetime_field)
        date_filter = {}
        date_filter[date_query] = self.get_time_edges()
        # Merge the dicts
        overall_filter = dict(filter_dict_mapped, **date_filter)
        return self.get_class().objects.filter(**overall_filter).order_by(self.datetime_field)

    def data_list(self):
        data_array = []
        # User.objects.extra({'date_created': "date(date_joined)"}).values('date_created').annotate(created_count=Count('id'))
        
        time_range, time_interval_count = self.get_time_range()

        points = self.data_points()
        for index, curr_time in enumerate(time_range):
            if index + 1 == len(time_range): continue
            date_filter = {str("%s__range" % self.datetime_field): (curr_time, time_range[index+1])}
            data_array.append((str(curr_time), points.filter(**date_filter).count()))
        return data_array, time_interval_count

    def get_time_range(self):
        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, now.day)
        if self.time_period == 'DA':
            time_range = [today + datetime.timedelta(minutes=10*x) for x in range(0, now.hour*6 + now.minute/10)]
            return time_range, now.hour/4
        elif self.time_period == 'WE':
            # TODO change this from 24*6 to the curr week
            time_range = [now - datetime.timedelta(hours=x) for x in range(0, now.hour + 24*6)]
            time_range.reverse()
            return time_range, 7#12 + now.hour/12

    @property
    def loader_top(self):
        return (self.height - LOADING_IMG_HEIGHT) / 2.0

    @property
    def loader_left(self):
        return (self.width - LOADING_IMG_WIDTH) / 2.0

