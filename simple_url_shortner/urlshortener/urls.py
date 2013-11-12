from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from .views import register_user
from django.contrib.auth.forms import UserCreationForm

urlpatterns = patterns(
    'urlshortener.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<short_code>\w+)$', 'redirect', name='redirect'),

    # auth views
    url(r'^login/$', login,
        {'template_name': 'login.html',
         'extra_context': {'user_register_form': UserCreationForm}},
        name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^register/$', register_user, name='register'),
)
