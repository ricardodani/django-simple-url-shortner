# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings

from .converter import num_to_base62


class Url(models.Model):
    '''
    Model representing a shortened URL.
    '''
    original_url = models.URLField()
    short_code = models.CharField(max_length=20, db_index=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        if self.short_code:
            return u'%s -> %s' % (self.original_url, self.get_absolute_url())
        else:
            return u'Not generated URL'

    def get_absolute_url(self):
        return settings.SITE_URL + reverse('redirect', args=[self.short_code])

    def save(self, *args, **kwargs):
        super(Url, self).save(*args, **kwargs)
        Url.objects.filter(id=self.id).update(
            short_code=num_to_base62(self.id)
        )
        self.short_code = num_to_base62(self.id)


    class Meta:
        ordering = ['-created_at']
