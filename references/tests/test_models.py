from django.test import TestCase
from references.models import BookReference, Reference, FilmReference, SiteReference, ArticleReference

REFERENCE_TYPES = [BookReference, FilmReference, SiteReference, ArticleReference]


class ReferencesModelsTests(TestCase):
    def test_get_types(self):
        expected = REFERENCE_TYPES
        actual = Reference.get_types()
        self.assertItemsEqual(expected, actual)

        choices = Reference.get_type_choices()
        self.assertEqual(len(choices), 4, "there are 4 types")
        self.assertIn(('book', 'Book'), Reference.get_type_choices())

        self.assertIn(('book', BookReference), Reference.get_type_mapping().items())

    def test_can_create_reference(self):
        with self.assertRaises(TypeError, msg="should prevent creating abstrace reference"):
            Reference.objects.create(
                name='Book 1',
                url='http://book1.com',
            )

        for reference_type in REFERENCE_TYPES:
            reference_type.objects.create(
                name='my reference',
            )

        self.assertEqual(Reference.objects.count(), 4, "all 4 instances should have been created")
