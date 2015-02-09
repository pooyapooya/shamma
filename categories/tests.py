from django.test import TestCase

# Create your tests here.
from categories.models import Topic


class TopicCreateTestCase(TestCase):
    def setUp(self):
        pass

    def topic_can_create(self):
        Topic.objects.create(name='Agile', parent=None)
        self.assert_(True, 'Agile topic created successfully')
        
