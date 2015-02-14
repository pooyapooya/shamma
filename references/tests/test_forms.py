from django.test import TestCase
from references.forms import CreateReferenceForm
from references.models import BookReference


class FormsTestCase(TestCase):
    def test_init_create_reference_form(self):
        self.assertIn('input', CreateReferenceForm().as_p())

    def valid_create_form_data(self):
        return {
            'name': 'Reference',
            'reference_type': 'book',
            'description': 'This is a nice book!',
        }

    def test_valid_create_reference_form(self):
        reference_form = CreateReferenceForm(data={})
        self.assertFalse(reference_form.is_valid(), "empty data is invalid")

        reference_form = CreateReferenceForm(data=self.valid_create_form_data())
        self.assertTrue(reference_form.is_valid(), "valid data should be ok")

    def test_save_create_reference_form(self):
        data = self.valid_create_form_data()
        form = CreateReferenceForm(data=data)
        form.is_valid()
        reference = form.save()
        self.assertIsInstance(reference, BookReference, "correct instance should be returned")

