# -*- coding: utf-8 -*-

import sys
from django.db import models
from django.contrib.auth.models import User


class Url(models.Model):
    '''
    Model representing a shortened URL.
    '''
    url = models.URLField()
    # short_code = models.CharField(max_length)
    user = models.ForeignKey(User, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
