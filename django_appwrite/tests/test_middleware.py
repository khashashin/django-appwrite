from django.test import RequestFactory, TestCase
from unittest.mock import patch
from django.contrib.sessions.middleware import SessionMiddleware
from django_appwrite.middleware import AppwriteMiddleware


class AppwriteMiddlewareTestCase(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.middleware = AppwriteMiddleware(lambda x: x)
        self.session_middleware = SessionMiddleware(lambda x: x)

    def test_settings_attribute_error(self):
        with self.assertRaises(Exception) as context:
            with self.settings(APPWRITE={}):
                self.middleware = AppwriteMiddleware(lambda x: x)

        self.assertIn("Make sure you have the following settings in your Django settings file", str(context.exception))

    @patch('appwrite.services.users.Users.get')
    def test_user_id_header_exists(self, mock_get_user_info):
        mock_get_user_info.return_value = {
            'email': 'test_user@example.com'
        }
        request = self.request_factory.get('/')
        request.META['USER_ID'] = 'test_user_id'

        response = self.middleware(request)
        self.assertEqual(response, request)
        self.assertTrue(request.user.is_authenticated)
        self.assertEqual(request.user.username, 'test_user@example.com')

    def test_user_id_header_not_exists(self):
        request = self.request_factory.get('/')
        response = self.middleware(request)
        self.assertEqual(response, request)
        self.assertFalse(request.user.is_authenticated)
