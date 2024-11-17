from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserModelTests(TestCase):

    def setUp(self):
        User.objects.all().delete()

    def test_creates_user_without_optional_fields(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.assertIsNone(user.bio)
        self.assertIsNone(user.google_id)

    def test_creates_user_with_bio(self):
        user = User.objects.create_user(username='testuser', password='12345', bio='This is a bio')
        self.assertEqual(user.bio, 'This is a bio')

    def test_creates_user_with_google_id(self):
        user = User.objects.create_user(username='testuser', password='12345', google_id='google123')
        self.assertEqual(user.google_id, 'google123')

    def test_updates_user_bio(self):
        user = User.objects.create_user(username='testuser', password='12345')
        User.objects.filter(id=user.id).update(bio='Updated bio')

        user = User.objects.get(id=user.id)
        self.assertEqual(user.bio, 'Updated bio')

    def test_updates_user_password(self):
        user = User.objects.create_user(username='testuser', password='12345')
        user.set_password('newpassword123')
        user.save()

        # Refresh the user object to get the updated password
        user.refresh_from_db(fields=['password'])

        self.assertTrue(user.check_password('newpassword123'))

    def test_updates_user_google_id(self):
        user = User.objects.create_user(username='testuser', password='12345')
        user.google_id = 'newgoogle123'
        user.save()
        self.assertEqual(user.google_id, 'newgoogle123')

    def test_deletes_user(self):
        user = User.objects.create_user(username='testuser', password='12345')
        user.delete()
        self.assertEqual(User.objects.filter(id=user.id).count(), 0)

    def test_gets_user_by_username(self):
        user = User.objects.create_user(username='testuser', password='12345')
        found_user = User.objects.get(username='testuser')
        self.assertEqual(user.id, found_user.id)

    def test_user_full_name(self):
        user = User.objects.create_user(username='testuser', password='12345', first_name='Test', last_name='User')
        self.assertEqual(user.get_full_name(), 'Test User')

    def test_user_short_name(self):
        user = User.objects.create_user(username='testuser', password='12345', first_name='Test')
        self.assertEqual(user.get_short_name(), 'Test')

    def test_user_email_normalization(self):
        user = User.objects.create_user(username='testuser', email='TEST@EMAIL.COM', password='12345')
        self.assertEqual(user.email, 'TEST@email.com')

    def test_create_superuser(self):
        user = User.objects.create_superuser(username='admin', email='admin@example.com', password='admin123')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class UserViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', email='testuser@example.com')
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123',
                                                        email='admin@example.com')
        self.client.login(username='testuser', password='12345')

    def test_list_users(self):
        self.client.force_authenticate(user=self.admin_user)
        url = '/users/list'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_users_unauthorized(self):
        url = '/users/list'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login(self):
        url = '/users/login'
        data = {'username': 'testuser', 'password': '12345'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_logout(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.force_authenticate(user=self.user)
        url = '/users/logout'
        data = {'refresh': str(refresh)}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_unauthorized(self):
        refresh = RefreshToken.for_user(self.user)
        url = '/users/logout'
        data = {'refresh': str(refresh)}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user(self):
        self.client.force_authenticate(user=self.user)
        url = '/users/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_signup(self):
        url = '/users/signup'
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'newuser@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)

    def test_get_user_by_id(self):
        self.client.force_authenticate(user=self.user)
        url = f'/users/user/{self.user.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_get_user_by_id_unauthorized(self):
        other_user = User.objects.create_user(username='otheruser', password='12345', email="testingemail12311312@example.com")
        url = f'/users/user/{other_user.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_self(self):
        self.client.force_authenticate(user=self.user)
        url = '/users/update'
        data = {'user_id': self.user.id, 'bio': 'Updated bio'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, 'Updated bio')

    def test_update_other_user_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        other_user = User.objects.create_user(username='otheruser', password='12345', email='someotheruser@example.com')
        url = '/users/update'
        data = {'user_id': other_user.id, 'bio': 'Updated bio'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        other_user.refresh_from_db()
        print(other_user.bio)
        self.assertEqual(other_user.bio, 'Updated bio')

    def test_update_other_user_unauthorized(self):
        self.client.force_authenticate(user=self.user)
        other_user = User.objects.create_user(username='otheruser', password='12345', email='otheruser@example.com')
        url = '/users/update'
        data = {'user_id': other_user.id, 'bio': 'Updated bio'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user(self):
        self.client.force_authenticate(user=self.admin_user)
        url = '/users/delete'
        data = {'user_id': self.user.id}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.filter(id=self.user.id).count(), 0)

    def test_delete_other_user(self):
        self.client.force_authenticate(user=self.user)
        other_user = User.objects.create_user(username='otheruser', password='12345', email='otheruser@example.com')
        url = '/users/delete'
        data = {'user_id': other_user.id}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_self(self):
        self.client.force_authenticate(user=self.user)
        url = '/users/delete'
        data = {'user_id': self.user.id}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.filter(id=self.user.id).count(), 0)
