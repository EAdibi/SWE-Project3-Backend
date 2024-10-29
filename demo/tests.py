from django.test import TestCase

from rest_framework.test import APITestCase, APIClient


# Create your tests here.
# Showing how to test API endpoints
class TestHelloWorld(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_hello_world(self):
        response = self.client.get('/demo/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'Hello, world!')

    def test_hello_user(self):
        response = self.client.get('/demo/User')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'Hello, User!')

    def test_hello_dictionary(self):
        response = self.client.get('/demo/test/dictionary')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"My custom Message Name": "Hello, world!"})