UNDER DEVELOPMENT

=======
Install
=======

Use pip::

	pip install django-dashboard --upgrade

or setuptools::

	easy_install -U django-dashboard

Add django-dashboard to the installed apps in your settings.py::

	INSTALLED_APPS = (
	    'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',

	    'dashboard',
	    ...
	)

Add the dashboard to your urls file::

	urlpatterns = patterns('',
	    ...
	    (r'^dashboard/', include('dashboard.urls')),
	    ...
	)

Finally, migrate with South::

	./manage.py migrate dashboard

=====
Usage
=====

Go to the Django admin and create a new dashbaord. Then create create a widget or two associated with that dashboard. Finally, go to YOURSITE.COM/dashboard/DASHBOARD_NAME/ to see the dashboard.


