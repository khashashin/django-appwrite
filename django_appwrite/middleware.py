from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.conf import settings
from appwrite.client import Client
from appwrite.services.account import Account
from django.utils.deprecation import MiddlewareMixin

User = get_user_model()


class AppwriteMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

        # Try to retrieve the required Appwrite settings from the Django settings file
        try:
            project_endpoint = settings.APPWRITE.get('PROJECT_ENDPOINT')
            project_id = settings.APPWRITE.get('PROJECT_ID')
            project_key = settings.APPWRITE.get('PROJECT_API_KEY')
            self.auth_header = settings.APPWRITE.get('AUTH_HEADER', 'HTTP_AUTHORIZATION')
            self.user_id_header = settings.APPWRITE.get('USER_ID_HEADER', 'HTTP_USER_ID')
            self.verify_email = settings.APPWRITE.get('VERIFY_EMAIL', False)
            self.verify_phone = settings.APPWRITE.get('VERIFY_PHONE', False)
        except AttributeError:
            raise Exception("""
                Make sure you have the following settings in your Django settings file:
                APPWRITE = {
                    'PROJECT_ENDPOINT': 'https://example.com/v1',
                    'PROJECT_ID': 'PROJECT_ID',
                    'PROJECT_API_KEY': 'PROJECT_API_KEY',
                    'USER_ID_HEADER': '[USER_ID]',
                }
            """)

        # Initialize Appwrite client
        self.client = (Client()
                       .set_endpoint(project_endpoint)
                       .set_project(project_id)
                       .set_key(project_key))

    def __call__(self, request, *args, **kwargs):
        try:
            # Get the user ID from the header
            user_id = request.META.get(self.user_id_header, '')
            auth_header = request.META.get(self.auth_header, '')
            jwt = auth_header.replace('Bearer ', '')
        except Exception as e:
            return self.get_response(request)

        user_info = None
        # If the user ID header is present
        if user_id and jwt:
            try:
                # Get the user information from Appwrite
                self.client.set_jwt(jwt)
                user_info = Account(self.client).get()
            except Exception as e:
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

            email = user_info['email']
            password = settings.SECRET_KEY+user_id
            # Get the Django user by its email
            user = User.objects.filter(username=email).first()

            # If the user doesn't exist, create it
            if not user:
                user = User.objects.create_user(
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
