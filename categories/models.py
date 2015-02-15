from collections import defaultdict
from django.db import models

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('categories.Topic', related_name='topics', null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_suggested_references(self):
        suggestions = defaultdict(list)
        for suggestion in self.suggestion_set.all():
            suggestions[suggestion.reference].append(suggestion.user)
        return suggestions.items()


class Suggestion(models.Model):
    user = models.ForeignKey('auth.User')
    topic = models.ForeignKey('categories.Topic')
    reference = models.ForeignKey('references.Reference')
