from django.test import TestCase

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