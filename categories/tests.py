import django
from django.test import TestCase

# Create your tests here.
from django.test.client import RequestFactory, Client
import json
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

    def test_get_data(self):
        c = Client()
        response = c.get('/categories/get_data/')
        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 2)

        agile = (topic for topic in json_response if topic['name'] == 'Agile').next()
        self.assertEqual(agile['parent'], None)

        scrum = (topic for topic in json_response if topic['name'] == 'Scrum').next()
        self.assertEqual(scrum['parent'], agile['id'])
