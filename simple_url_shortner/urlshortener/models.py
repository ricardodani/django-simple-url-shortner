# -*- coding: utf-8 -*-

import sys
from django.db import models
from django.contrib.auth.models import User
from .converter import num_to_base62


class Url(models.Model):
    '''
    Model representing a shortened URL.
    '''
    url = models.URLField()
    short_code = models.CharField(max_length=20, db_index=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s => %s' % (self.short_code, self.url)

    def save(self, *args, **kwargs):
        super(Url, self).save(*args, **kwargs)
        Url.objects.filter(id=self.id).update(short_code=num_to_base62(self.id))

    class Meta:
        ordering = ['-created_at']
