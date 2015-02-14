from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from references.models import BookReference


class CreateReferenceViewTestCase(TestCase):
    def setup(self):
        self.client = Client()
        super(CreateReferenceViewTestCase, self).setup()

    def test_get(self):
        response = self.client.get(reverse('create_reference'))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(reverse('create_reference'), {
            'reference_type': 'book',
            'name': 'new_book',
        })
        self.assertEqual(response.status_code, 302, "should redirect to reference_view")
        self.assertEqual(BookReference.objects.count(), 1)
