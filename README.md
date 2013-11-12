django-simple-url-shortner
==========================

A simple URL Shortner project written in python/django.

Configure
---------

Configure your cache backend on CACHES directive in settings.
Example:

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }

Install
-------

Requirements:

    pip install -r requeriments.txt

Tests:

    python manage.py test

Sync database:

    python manage.py syncdb

Runserver:

    python manage.py runserver
