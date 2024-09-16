from django.db import models


class DiskLink(models.Model):
    public_key = models.CharField(max_length=255, unique=True)

