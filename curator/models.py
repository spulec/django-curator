import ast
import calendar
import datetime

from django.conf import settings
from django.db import models, DEFAULT_DB_ALIAS
from django.db.models import Count

from curator.utils import get_class, get_datetime_fields

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
    ('28', '28 Days'),
    ('YR', 'Year'),
    ('36', '365 Days'),
    #('AT', 'All Time'),
)

TIME_FILTER_DICT = {
    'minute': "%m/%d/%Y %H %M",
    'hour': "%m/%d/%Y %H",
    'day': "%m/%d/%Y",
    'month': "%m/%Y",
}

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

def get_db_alias():
    engine = settings.DATABASES[DEFAULT_DB_ALIAS]['ENGINE']
    return ENGINE_MODULES.get(engine, None)

# Implementing this because it wasn't added until Python 2.7
def timestamp_to_seconds(timestamp):
    return int((timestamp.microseconds + (timestamp.seconds + timestamp.days * 24 * 3600) * 10**6) / 10.0**6)


DB_ALIAS = get_db_alias()
LOADING_IMG_HEIGHT = 19
LOADING_IMG_WIDTH = 220
        
class Dashboard(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class DashboardWidget(models.Model):
    dashboard = models.ForeignKey(Dashboard)
    model = models.CharField(max_length=255, choices=MODEL_CHOICES)
    filter_dict = models.CharField(max_length=255, blank=True, null=True, help_text="e.g.  {'is_active': True, 'username__contains':'steve'}")
    time_period = models.CharField(max_length=2, choices=TIME_PERIOD_CHOICES)
    datetime_field = models.CharField(max_length=255)
    order = models.IntegerField(null=True)
    height = models.IntegerField(default=200)
    width = models.IntegerField(default=400)

    def __unicode__(self):
        return "%s : %s" % (self.dashboard, self.model)

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = self.dashboard.dashboardwidget_set.count()
        super(DashboardWidget, self).save(*args, **kwargs)

    def get_select_data(self, time_filter):
        
        select_filter_dict = {
            'sqlite3': "strftime('%s', %s)" % (time_filter, self.datetime_field),
            'mysql': "DATE_FORMAT(%s, '%s')" % (self.datetime_field, time_filter.replace("M", "i")),
        }

        select_filter = select_filter_dict.get(DB_ALIAS, None)
        if not select_filter:
            NotImplemented
        
        return {"datetime": select_filter}
    
    def data_points(self):
        filter_dict = ast.literal_eval(self.filter_dict) if self.filter_dict else {}
        return get_class(self.model).objects.filter(**filter_dict).order_by(self.datetime_field)
        
    def data_list(self):
        time_range, prev_time_range, time_interval = self.get_time_range()
        time_filter = TIME_FILTER_DICT[time_interval]
        prev_time_offset = timestamp_to_seconds(time_range[0] - prev_time_range[0])

        data_array = self.datetimes_to_array(time_range, time_filter)
        prev_data_array = self.datetimes_to_array(prev_time_range, time_filter, prev_time_offset)

        return data_array, prev_data_array, time_interval, prev_time_offset

    def datetimes_to_array(self, time_range, time_filter, offset=0):
        escaped_time_filter = time_filter.replace("%", "%%")
        select_data = self.get_select_data(escaped_time_filter)
        date_filter = {str("%s__range" % self.datetime_field): (time_range[0], time_range[-1])}

        data_map = {}
        for index, curr_time in enumerate(time_range):
            # Convert to string and back to lose datetime precision
            curr_time = datetime.datetime.strptime(curr_time.strftime(time_filter), time_filter)
            # Convert time_range to timestamps
            curr_time = str(int(curr_time.strftime("%s")) + offset)
            data_map[curr_time] = 0
        points = self.data_points().filter(**date_filter).extra(select=select_data).values('datetime').annotate(count=Count(self.datetime_field)).order_by()
        for point in points:
            point_datetime = datetime.datetime.strptime(point['datetime'], time_filter)
            data_map[str(int(point_datetime.strftime("%s")) + offset)] = point['count']
        data_array = data_map.items()
        data_array.sort()
        return data_array
    
    def get_time_range(self):
        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, now.day)
        
        # Set first weekday to Sunday
        calendar.setfirstweekday(6)
        
        prev_range = []
        if self.time_period == 'DA':
            time_range = [today + datetime.timedelta(minutes=10*x) for x in range(now.hour*6 + now.minute/10 + 1)]
            prev_range = [time - datetime.timedelta(days=7) for time in time_range]
            time_interval = 'minute'
        elif self.time_period == '24':
            time_range = [now - datetime.timedelta(minutes=10*x) for x in range(24 * 6 + 1)]
            time_range.reverse()
            prev_range = [time - datetime.timedelta(days=7) for time in time_range]
            time_interval = 'minute'
        elif self.time_period == 'WE':
            day_of_week = calendar.weekday(now.year, now.month, now.day)
            first_week_day = today - datetime.timedelta(days=day_of_week)
            time_range = [first_week_day + datetime.timedelta(hours=x) for x in range(now.hour + day_of_week * 24 + 1)]
            prev_range = [time - datetime.timedelta(days=7) for time in time_range]
            time_interval = 'hour'
        elif self.time_period == '7D':
            time_range = [now - datetime.timedelta(hours=x) for x in range(24 * 7 + 1)]
            time_range.reverse()
            prev_range = [time - datetime.timedelta(days=7) for time in time_range]
            time_interval = 'hour'
        elif self.time_period == 'MO':
            first_month_day = datetime.datetime(now.year, now.month, 1)
            time_range = [first_month_day + datetime.timedelta(days=x) for x in range(now.day + 1)]
            if now.month == 1:
                prev_first_month_day = datetime.datetime(now.year - 1, 12, 1)
            else:
                prev_first_month_day = datetime.datetime(now.year, now.month - 1, 1)
            #TODO fix bug here if previous month has less days than this one
            prev_range = [prev_first_month_day + datetime.timedelta(days=x) for x in range(now.day + 1)]
            time_interval = 'day'
        elif self.time_period == '28':
            time_range = [now - datetime.timedelta(days=x) for x in range(28 + 1)]
            time_range.reverse()
            prev_range = [time - datetime.timedelta(days=28) for time in time_range]
            time_interval = 'day'
        elif self.time_period == 'YR':
            first_year_day = datetime.datetime(now.year, 1, 1)
            day_of_year = now.timetuple().tm_yday
            time_range = [first_year_day + datetime.timedelta(days=10 * x) for x in range(day_of_year/10 + 1)]
            prev_first_year_day = datetime.datetime(now.year - 1, 1, 1)
            prev_range = [prev_first_year_day + datetime.timedelta(days=10 * x) for x in range(day_of_year/10 + 1)]
            time_interval = 'month'
        elif self.time_period == '36':
            time_range = [now - datetime.timedelta(days=365) for x in range(365 + 1)]
            time_range.reverse()
            prev_range = [time - datetime.timedelta(days=365) for time in time_range]
            time_interval = 'month'
        return time_range, prev_range, time_interval
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

