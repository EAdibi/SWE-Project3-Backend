from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import Lesson

class LessonViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', email='testuser@example.com')
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123', email='admin@example.com')
        self.client.login(username='testuser', password='12345')

    def test_list_all_lessons(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_all_lessons_unauthorized(self):
        response = self.client.get('/lessons/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Lesson',
            'description': 'Lesson Description',
            'category': 'Category',
            'is_public': True
        }
        response = self.client.post('/lessons/new', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_lesson_missing_fields(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Lesson'
        }
        response = self.client.post('/lessons/new', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_lesson_unauthorized(self):
        data = {
            'title': 'New Lesson',
            'description': 'Lesson Description',
            'category': 'Category',
            'is_public': True
        }
        response = self.client.post('/lessons/new', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_public_lessons(self):
        response = self.client.get('/lessons/public')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_lessons_by_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/lessons/user/{self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_lessons_by_user_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/lessons/user/999')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_lessons_by_category(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/lessons/category/Category')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_lessons_by_keywords(self):
        self.client.force_authenticate(user=self.user)
        Lesson.objects.create(title='New Lesson', description='Lesson Description', category='Category', created_by=self.user)
        response = self.client.get('/lessons/keywords/New')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.user)
        lesson = Lesson.objects.create(title='Old Title', description='Old Description', category='Category', created_by=self.user)
        data = {
            'lesson_id': lesson.id,
            'title': 'Updated Title'
        }
        response = self.client.patch('/lessons/update', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson_unauthorized(self):
        lesson = Lesson.objects.create(title='Old Title', description='Old Description', category='Category', created_by=self.user)
        data = {
            'lesson_id': lesson.id,
            'title': 'Updated Title'
        }
        response = self.client.patch('/lessons/update', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.user)
        lesson = Lesson.objects.create(title='Old Title', description='Old Description', category='Category', created_by=self.user)
        data = {
            'lesson_id': lesson.id
        }
        response = self.client.delete('/lessons/delete', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson_unauthorized(self):
        lesson = Lesson.objects.create(title='Old Title', description='Old Description', category='Category', created_by=self.user)
        data = {
            'lesson_id': lesson.id
        }
        response = self.client.delete('/lessons/delete', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)