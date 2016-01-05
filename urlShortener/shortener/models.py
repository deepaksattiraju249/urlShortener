from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Url(models.Model):
	shortenedUrl = models.CharField(max_length=100)
	actualUrl = models.CharField(max_length=200)
