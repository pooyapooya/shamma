import django
from django.test import TestCase

# Create your tests here.
from django.test.client import RequestFactory, Client
from categories.models import Topic


class TopicTestCase(TestCase):
    def setUp(self):
        pass

    def topic_can_create_and_delete(self):
        Topic.objects.create(name='Agile', parent=None)
        self.assert_(True, 'Agile topic created successfully')
        topics = Topic.objects.get(name='Agile')
        self.assertEqual(topics.id, 1)
        topics.delete()
        topics = Topic.objects.filter(name='Agile')
        self.assertFalse(topics, 'Everything is correct')


class GetCategoriesJson(TestCase):
    def setUp(self):
        super(GetCategoriesJson, self).setUp()
        par = Topic.objects.create(name='Agile', parent=None)
        Topic.objects.create(name='Scrum', parent=par)

    def check_json(self):
        # rf = RequestFactory()
        # get_request = rf.get('/get_data/')
        # print json
        c = Client()
        json = c.get('/categories/get_data/')
        print json.body
        self.assert_('Ok.')