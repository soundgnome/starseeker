from django.test import TestCase
from django.contrib.auth import get_user_model


class UserTestCase(TestCase):

    def setUp(self):
        self.user_model = get_user_model()

    def test_user_fields(self):
        self.assertEqual(self.user_model.USERNAME_FIELD, 'email')

    def test_user_status(self):
        user = self.user_model.objects.get(username='testuser@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
