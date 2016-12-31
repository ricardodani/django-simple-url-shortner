django-simple-url-shortner
==========================

A simple URL Shortner project written in python/django.

Screenshots
-----------

![Create](/screenshots/create.png "Create")

![Created with Success](/screenshots/create_success.png "Created with success")

![Index Logged in](/screenshots/index_logged_in.png "Index page logged in")

![Login page](/screenshots/login_page.png "Login page")

![Register modal](/screenshots/register_modal.png "Register modal")

![Register page](/screenshots/register_page.png "Register page")

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

    python manage.py makemigrations urlshortner
    python manage.py migrate

Runserver:

    python manage.py runserver

Support on Windows with Django 1.10
-----------------------------------

Contributor: Samuel Dias
             Ricardo Lapa Dani

Configuring CACHE on settings.py using DatabaseCache instead of Memcached (not supported by Windows):

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'my_cache_table',
        }
    }

Sync database:

    python manage.py createcachetable