from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'simple_url_shortner.views.home', name='home'),

    url(r'^', include('urlshortener.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
