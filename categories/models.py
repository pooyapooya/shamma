from django.db import models

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('categories.Topic', related_name='topics', null=True, blank=True)

    def __unicode__(self):
        return self.name
