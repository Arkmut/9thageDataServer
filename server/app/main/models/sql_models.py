from django.db import models


class PublicArmy(models.Model):
    name = models.CharField(unique=True, primary_key=True)
    version = models.CharField(blank=False)
