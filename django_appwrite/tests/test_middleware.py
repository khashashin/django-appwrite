from django.test import RequestFactory, TestCase
from unittest.mock import patch
from django_appwrite.middleware import AppwriteMiddleware


class AppwriteMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.middleware = AppwriteMiddleware(self.request)

    def test_settings_attribute_error(self):
        with self.assertRaises(Exception) as context:
            with self.modify_settings(APPWRITE={}):
                self.middleware = AppwriteMiddleware(self.request)

        self.assertIn("Make sure you have the following settings in your Django settings file", str(context.exception))

    @patch('appwrite.services.users.Users.get')
    def test_user_id_header_exists(self, mock_get_user_info):
        mock_get_user_info.return_value = {
            'email': 'test_user@example.com'
        }
        request = self.factory.get('/')
        request.META['HTTP_USER_ID'] = 'test_user_id'

        response = self.middleware(request)
        self.assertEqual(response, request)
        self.assertTrue(response.user.is_authenticated)
        self.assertEqual(response.user.username, 'test_user@example.com')

    def test_user_id_header_not_exists(self):
        request = self.factory.get('/')
        response = self.middleware(request)
        self.assertEqual(response, request)
        self.assertFalse(hasattr(response, 'user'))
