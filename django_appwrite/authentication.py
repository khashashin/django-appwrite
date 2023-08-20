from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model, authenticate
from appwrite.services.account import Account

from django_appwrite.utilities import initialize_appwrite_client, get_appwrite_settings, log_error

User = get_user_model()


class AppwriteAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Extract the Appwrite token from the request headers
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None  # No authentication attempt

        token = auth_header.split('Bearer ')[1]

        # Verify the token with Appwrite
        client = initialize_appwrite_client()
        client.set_jwt(token)

        try:
            user_info = Account(client).get()
        except Exception as e:
            if settings.DEBUG:
                log_error(e)
            raise AuthenticationFailed('Invalid Appwrite token or other Appwrite authentication issue.')

        appwrite_settings = get_appwrite_settings()

        email = appwrite_settings['prefix_email'] + user_info['email']
        password = settings.SECRET_KEY + user_info['$id']

        username_field = getattr(User, 'USERNAME_FIELD', 'username')

        # Get or create a corresponding Django user
        django_user = User.objects.filter(**{username_field: email}).first()
        if not django_user:
            User.objects.create_user(**{username_field: email, 'password': password})

        # Ensure the user can be authenticated with Django's system
        auth_user = authenticate(request, **{username_field: email, 'password': password})
        if not auth_user:
            raise AuthenticationFailed('The user could not be authenticated with Django.')

        return auth_user, token
