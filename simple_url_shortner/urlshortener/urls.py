from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout

urlpatterns = patterns(
    'urlshortener.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<short_code>\w+)$', 'redirect', name='redirect'),
    url(r'^login/$', login, {'template_name': 'index.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
)
