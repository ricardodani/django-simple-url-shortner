from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from .views import register_user

urlpatterns = patterns(
    'urlshortener.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<short_code>\w+)$', 'redirect', name='redirect'),

    # auth views
    url(r'^login/$', login, {'template_name': 'index.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^register/$', register_user, name='register'),
)
