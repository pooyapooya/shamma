from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from mock import patch
from accounts.models import UserProfile


class UserModelTest(TestCase):
    def test_creating_a_new_user_and_saving_it_to_the_database(self):
        user = User()
        user.username = "_sajad"
        user.password = "1234"
        user.email = "asdf@asdf.com"
        user.is_active = False
        user.save()

        user_profile = UserProfile()

        user_profile.user = user

        # check we can save it to the databaseg

        user_profile.save()

        # now check we can find it in the database again
        user = User.objects.get(username__contains="sajad")
        self.assertEqual(user.email, "asdf@asdf.com")
        self.assertEqual(user.is_active, False)

    def test_register_user_login(self):
        c = Client()
        response = c.post('/accounts/register/',
                          {'username': 'sjn', 'password': 'asdfasdf', 'email': 'sajad22@gmail.com'})
        self.assertEqual(200, response.status_code)
        user = User.objects.get(username__contains="sjn")
        self.assertEqual(user.is_active, False)
        d = Client()
        response = d.get('/accounts/confirm/' + user.userprofile.activation_key + '/')
        user = User.objects.get(username__contains="sjn")
        self.assertEqual(user.is_active, True)
        g = Client()
        response = g.post('/accounts/login/',
                          {'username': 'sj2n', 'password': 'asdfasdf'})
        self.assertNotEqual(302, response.status_code)
        f = Client()
        response = f.post('/accounts/login/',
                          {'username': 'sjn', 'password': 'asdfasdf'})
        self.assertEqual(302, response.status_code)

    def test_register_user_logout(self):
        c = Client()
        response = c.post('/accounts/register/',
                          {'username': 'sjn', 'password': 'asdfasdf', 'email': 'sajad22@gmail.com'})
        user = User.objects.get(username__contains="sjn")
        d = Client()
        response = d.get('/accounts/confirm/' + user.userprofile.activation_key + '/')
        user = User.objects.get(username__contains="sjn")
        f = Client()
        response = f.post('/accounts/login/',
                          {'username': 'sjn', 'password': 'asdfasdf'})
        g = Client()
        response = g.post('/accounts/logout/', {})
        self.assertEqual(301, response.status_code)

    def test_register_user_complete_profile(self):
        c = Client()
        response = c.post('/accounts/register/',
                          {'username': 'sjn', 'password': 'asdfasdf', 'email': 'sajad22@gmail.com'})
        user = User.objects.get(username__contains="sjn")
        d = Client()
        response = d.get('/accounts/confirm/' + user.userprofile.activation_key + '/')
        user = User.objects.get(username__contains="sjn")
        f = Client()
        response = f.post('/accounts/login/',
                          {'username': 'sjn', 'password': 'asdfasdf'})

        user = User.objects.get(username__contains="sjn")
        self.assertFalse(user.userprofile.is_complete_profile())
        response = f.post('/accounts/edit/', {'national_code': '1251355434', 'mobile_phone': '09123654530'})

        user = User.objects.get(username__contains="sjn")
        self.assertTrue(user.userprofile.is_complete_profile())
