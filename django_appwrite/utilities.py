from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from appwrite.client import Client
from appwrite.services.account import Account
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


def get_appwrite_settings():
    try:
        project_endpoint = settings.APPWRITE.get('PROJECT_ENDPOINT')
        project_id = settings.APPWRITE.get('PROJECT_ID')
        project_key = settings.APPWRITE.get('PROJECT_API_KEY')
        auth_header = settings.APPWRITE.get('AUTH_HEADER', 'HTTP_AUTHORIZATION')
        verify_email = settings.APPWRITE.get('VERIFY_EMAIL', False)
        verify_phone = settings.APPWRITE.get('VERIFY_PHONE', False)
        prefix_email = settings.APPWRITE.get('PREFIX_EMAIL', '')

        return {
            'project_endpoint': project_endpoint,
            'project_id': project_id,
            'project_key': project_key,
            'auth_header': auth_header,
            'verify_email': verify_email,
            'verify_phone': verify_phone,
            'prefix_email': prefix_email,
        }
    except AttributeError:
        raise Exception("""
            Make sure you have the following settings in your Django settings file:
            APPWRITE = {
                'PROJECT_ENDPOINT': 'https://example.com/v1',
                'PROJECT_ID': 'PROJECT_ID',
                'PROJECT_API_KEY': 'PROJECT_API_KEY',
            }
        """)


def initialize_appwrite_client():
    appwrite_settings = get_appwrite_settings()
    client = (Client().set_endpoint(appwrite_settings['project_endpoint'])
              .set_project(appwrite_settings['project_id'])
              .set_key(appwrite_settings['project_key']))
    return client


def log_error(e):
    import logging
    logger = logging.getLogger('django')
    logger.error('Error: ', e)


def check_verification(user_info, appwrite_settings):
    if appwrite_settings['verify_email'] and not user_info['emailVerification']:
        raise AuthenticationFailed('Email not verified.')
    if appwrite_settings['verify_phone'] and not user_info['phoneVerification']:
        raise AuthenticationFailed('Phone not verified.')


def get_or_create_django_user(request, user_info, appwrite_settings):
    email = appwrite_settings['prefix_email'] + user_info['email']
    password = settings.SECRET_KEY + user_info['$id']
    username_field = getattr(User, 'USERNAME_FIELD', 'username')

    # Get or create a corresponding Django user
    django_user = User.objects.filter(**{username_field: email}).first()
    if not django_user:
        User.objects.create_user(**{username_field: email, 'password': password})

    auth_user = authenticate(request, **{username_field: email, 'password': password})
    if not auth_user:
        raise AuthenticationFailed('The user could not be authenticated with Django.')

    return auth_user


def _log_error(message, exception=None):
    if settings.DEBUG:
        log_error(message)
        if exception:
            log_error(str(exception))


def get_appwrite_user_info(token):
    client = initialize_appwrite_client()
    client.set_jwt(token)
    try:
        return Account(client).get()
    except Exception as e:
        _log_error(e)
        raise AuthenticationFailed('Invalid Appwrite token or other Appwrite authentication issue.')


def extract_token(request, appwrite_settings):
    try:
        auth_header = request.headers.get(appwrite_settings['auth_header'])
        if not auth_header or 'Bearer ' not in auth_header:
            raise ValueError("Bearer token missing, make sure you're using the correct auth header.")
        return auth_header.split('Bearer ')[1]
    except (ValueError, IndexError) as e:
        _log_error('AppwriteAuthentication: cannot extract token from request headers.', e)
        return None
