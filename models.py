import ast
import calendar
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
    ('24', '24 Hours'),
    ('WE', 'Weekly'),
    ('7D', '7 Days'),
    ('MO', 'Monthly'),
    ('30', '30 Days'),
    ('YR', 'Year'),
    ('36', '365 Days'),
    ('AT', 'All Time'),
)

LOADING_IMG_HEIGHT = 19
LOADING_IMG_WIDTH = 220
        
# Set first weekday to Sunday
calendar.setfirstweekday(6)

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

    def data_points(self):
        filter_dict = ast.literal_eval(self.filter_dict) if self.filter_dict else {}
        return self.get_class().objects.filter(**filter_dict).order_by(self.datetime_field)
    
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
        elif self.time_period == '24':
            time_range = [now - datetime.timedelta(minutes=10*x) for x in range(0, 24 * 6)]
            time_range.reverse()
            return time_range, 6
        elif self.time_period == 'WE':
            first_week_day = today - datetime.timedelta(days=calendar.weekday(now.year, now.month, now.day))
            time_range = [first_week_day + datetime.timedelta(hours=x) for x in range(0, 7 * 24)]
            return time_range, 7
        elif self.time_period == '7D':
            time_range = [now - datetime.timedelta(hours=x) for x in range(0, now.hour + 24 * 6)]
            time_range.reverse()
            return time_range, 7
        elif self.time_period == 'MO':
            first_month_day = datetime.datetime(now.year, now.month, now.day)
            time_range = [first_month_day + datetime.timedelta(days=x) for x in range(0, now.day)]
            return time_range, now.day
        elif self.time_period == '30':
            time_range = [now - datetime.timedelta(days=x) for x in range(0, 30)]
            time_range.reverse()
            return time_range, 30
        elif self.time_period == 'YR':
            first_year_day = datetime.datetime(now.year, 1, 1)
            day_of_year = now.timetuple().tm_yday
            time_range = [first_year_day + datetime.timedelta(days=10 * x) for x in range(0, day_of_year/10)]
            return time_range, day_of_year / 10
        elif self.time_period == '36':
            time_range = [now - datetime.timedelta(days=365) for x in range(0, 365)]
            time_range.reverse()
            return time_range, 365
        """
        TODO
        ('AT', 'All Time'),
        """
    @property
    def loader_top(self):
        return (self.height - LOADING_IMG_HEIGHT) / 2.0

    @property
    def loader_left(self):
        return (self.width - LOADING_IMG_WIDTH) / 2.0

