from django.core.urlresolvers import reverse_lazy
from django.db import models
from polymorphic.polymorphic_model import PolymorphicModel


class Reference(PolymorphicModel):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    type_caption = 'AbstractReference'

    def save(self, *args, **kwargs):
        if type(self) == Reference:
            raise TypeError('Reference is abstract class. Use inherited classes instead')
        super(Reference, self).save(*args, **kwargs)

    @classmethod
    def get_type_id(cls):
        return cls.type_caption.lower()

    @staticmethod
    def get_types():
        return Reference.__subclasses__()

    @staticmethod
    def get_type_choices():
        return [(cls.get_type_id(), cls.type_caption) for cls in Reference.get_types()]

    @staticmethod
    def get_type_mapping():
        return {cls.get_type_id(): cls for cls in Reference.get_types()}

    def get_absolute_url(self):
        return reverse_lazy('reference_detail', kwargs={'pk': self.id})


class FilmReference(Reference):
    type_caption = 'Film'


class ArticleReference(Reference):
    type_caption = 'Article'


class BookReference(Reference):
    type_caption = 'Book'


class SiteReference(Reference):
    type_caption = 'Site'
