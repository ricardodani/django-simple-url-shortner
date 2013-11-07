from django.conf.urls import patterns, url

urlpatterns = patterns(
    'urlshortener.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<short_code>\w+)$', 'redirect', name='redirect'),
)
