from django.conf import settings
from appwrite.client import Client


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
