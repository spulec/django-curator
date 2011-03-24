import ast
import calendar
import datetime

from django.conf import settings
from django.db import models, DEFAULT_DB_ALIAS
from django.db.models import Count

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

ENGINE_MODULES = {
    'django.db.backends.postgresql_psycopg2': 'postgresql_psycopg2',
    'django.db.backends.sqlite3': 'sqlite3',
    'django.db.backends.mysql': 'mysql',
    'django.db.backends.oracle': 'oracle',
    'sql_server.pyodbc': 'sql_server.pyodbc', #django-pyodbc
    'sqlserver_ado': 'sql_server.pyodbc', #django-mssql
    'django.contrib.gis.db.backends.postgis': 'postgresql_psycopg2',
    'django.contrib.gis.db.backends.spatialite': 'sqlite3',
    'django.contrib.gis.db.backends.mysql': 'mysql',
    'django.contrib.gis.db.backends.oracle': 'oracle',
}

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

    def get_select_data(self, time_filter):
        engine = settings.DATABASES[DEFAULT_DB_ALIAS]['ENGINE']
        alias = ENGINE_MODULES.get(engine, None)

        if alias == 'sqlite3':
            select_filter = """%s('%s', %s)""" % ("strftime", time_filter, self.datetime_field)
        elif alias == 'mysql':
            select_filter = """%s(%s, '%s')""" % ("DATE_FORMAT", self.datetime_field, time_filter)
        else:
            NotImplemented
        
        return {"datetime": select_filter}
    

    def data_points(self):
        filter_dict = ast.literal_eval(self.filter_dict) if self.filter_dict else {}
        return self.get_class().objects.filter(**filter_dict).order_by(self.datetime_field)
    
    def data_list(self):
        data_map = {}
        
        time_range, time_filter, time_interval = self.get_time_range()

        date_filter = {str("%s__range" % self.datetime_field): (time_range[0], time_range[-1])}
        # Convert time_range to timestamps
        time_range = [time.strftime("%s") for time in time_range]
        
        for index, curr_time in enumerate(time_range):
            if index + 1 == len(time_range): continue
            data_map[curr_time] = 0

        select_data = self.get_select_data(time_filter)
        points = self.data_points().filter(**date_filter).extra(select=select_data).values('datetime').annotate(count=Count('id')).order_by()
        for point in points:
            point_datetime = datetime.datetime.strptime(point['datetime'], time_filter.replace("%%", "%"))
            data_map[point_datetime.strftime("%s")] = point['count']
        
        data_array = data_map.items()
        data_array.sort()
        return data_array, time_interval
    
    def get_time_range(self):
        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, now.day)
        # Set first weekday to Sunday
        calendar.setfirstweekday(6)
        
        if self.time_period == 'DA':
            time_range = [today + datetime.timedelta(minutes=10*x) for x in range(0, now.hour*6 + now.minute/10)]
            time_filter = "%%m/%%d/%%Y %%H %%M"
            return time_range, time_filter, 'minute' #now.hour/4
        elif self.time_period == '24':
            time_range = [now - datetime.timedelta(minutes=10*x) for x in range(0, 24 * 6)]
            time_range.reverse()
            time_filter = "%%m/%%d/%%Y %%H %%M"
            return time_range, time_filter, 'minute' #6
        elif self.time_period == 'WE':
            day_of_week = calendar.weekday(now.year, now.month, now.day)
            first_week_day = today - datetime.timedelta(days=day_of_week)
            time_range = [first_week_day + datetime.timedelta(hours=x) for x in range(0, now.hour + day_of_week * 24)]
            time_filter = "%%m/%%d/%%Y %%H"
            return time_range, time_filter, 'hour' #7
        elif self.time_period == '7D':
            time_range = [now - datetime.timedelta(hours=x) for x in range(0, 24 * 7)]
            time_range.reverse()
            time_filter = "%%m/%%d/%%Y %%H"
            return time_range, time_filter, 'hour' #7
        elif self.time_period == 'MO':
            first_month_day = datetime.datetime(now.year, now.month, 1)
            time_range = [first_month_day + datetime.timedelta(days=x) for x in range(0, now.day)]
            time_filter = "%%m/%%d/%%Y"
            return time_range, time_filter, 'day' #now.day
        elif self.time_period == '30':
            time_range = [now - datetime.timedelta(days=x) for x in range(0, 30)]
            time_range.reverse()
            time_filter = "%%m/%%d/%%Y"
            return time_range, time_filter, 'day' #30
        elif self.time_period == 'YR':
            first_year_day = datetime.datetime(now.year, 1, 1)
            day_of_year = now.timetuple().tm_yday
            time_range = [first_year_day + datetime.timedelta(days=10 * x) for x in range(0, day_of_year/10)]
            time_filter = "%%m/%%Y"
            return time_range, time_filter, 'month' #day_of_year / 10
        elif self.time_period == '36':
            time_range = [now - datetime.timedelta(days=365) for x in range(0, 365)]
            time_range.reverse()
            time_filter = "%%m/%%Y"
            return time_range, time_filter, 'month' #365
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

