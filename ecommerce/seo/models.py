from django.db import models

class SeoModel(models.Model):
    seo_title = models.CharField(max_length=70, blank=True, name=True)
    seo_description = models.CharField(max_length=300, blank=True, null=True)
    seo_tags = models.TextField(blank=True, null=True)
    class Meta:
        abstract = True