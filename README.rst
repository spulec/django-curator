UNDER DEVELOPMENT

=======
Install
=======

Use pip::

	pip install django-curator --upgrade

or setuptools::

	easy_install -U django-curator

Add django-curator to the installed apps in your settings.py::

	INSTALLED_APPS = (
	    'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',

	    'curator',
	    ...
	)

Add curator to your urls file::

	urlpatterns = patterns('',
	    ...
	    (r'^curator/', include('curator.urls')),
	    ...
	)

Finally, migrate with South::

	./manage.py migrate curator

=====
Usage
=====

Go to the Django admin and create a new dashboard. Then create create a widget or two associated with that dashboard. Finally, go to YOURSITE.COM/curator/DASHBOARD_NAME/ to see the dashboard.


