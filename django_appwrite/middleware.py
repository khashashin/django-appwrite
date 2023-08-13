from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.conf import settings
from appwrite.services.account import Account
from django.utils.deprecation import MiddlewareMixin

from .utilities import get_appwrite_settings, initialize_appwrite_client, log_error

User = get_user_model()


class AppwriteMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response
        appwrite_settings = get_appwrite_settings()

        self.auth_header = appwrite_settings['auth_header']
        self.verify_email = appwrite_settings['verify_email']
        self.verify_phone = appwrite_settings['verify_phone']
        self.prefix_email = appwrite_settings['prefix_email']

        # Initialize Appwrite client
        try:
            self.client = initialize_appwrite_client()
        except Exception as e:
            if settings.DEBUG:
                log_error(e)

    def __call__(self, request, *args, **kwargs):
        # Check if the Appwrite Authentication is enabled in DRF settings
        drf_auth_classes = getattr(settings, 'REST_FRAMEWORK', {}).get('DEFAULT_AUTHENTICATION_CLASSES', [])
        is_appwrite_auth_enabled = 'django_appwrite.authentication.AppwriteAuthentication' in drf_auth_classes

        # If Appwrite Authentication is not used in DRF, proceed with middleware authentication
        if not is_appwrite_auth_enabled:
            try:
                # Get the jwt from the header
                auth_header = request.META.get(self.auth_header, '')
                jwt = auth_header.replace('Bearer ', '')
            except Exception as e:
                if settings.DEBUG:
                    log_error(e)
                return self.get_response(request)

            user_info = None
            # If the jwt header is present
            if jwt:
                try:
                    # Get the user information from Appwrite
                    self.client.set_jwt(jwt)
                    user_info = Account(self.client).get()
                except Exception as e:
                    if settings.DEBUG:
                        log_error(e)
                    # Return the response without doing anything
                    return self.get_response(request)

            # If the user information was retrieved successfully
            if user_info:

                # If the user has not verified their email, return the response without doing anything
                if self.verify_email and not user_info['emailVerification']:
                    return self.get_response(request)

                # If the user has not verified their phone, return the response without doing anything
                if self.verify_phone and not user_info['phoneVerification']:
                    return self.get_response(request)

                email = self.prefix_email + user_info['email']
                password = settings.SECRET_KEY + user_info['$id']
                # Get the Django user by its email
                user = User.objects.filter(username=email).first()

                # If the user doesn't exist, create it
                if not user:
                    User.objects.create_user(
                        username=email,
                        password=password,
                        email=email)

                # Authenticate the user using the email as the username
                user = authenticate(request, username=email, password=password)

                # If the authentication was successful, log the user in
                if user:
                    request.user = user
                    login(request, user)

        # Call the next middleware/view in the pipeline
        response = self.get_response(request)

        return response
