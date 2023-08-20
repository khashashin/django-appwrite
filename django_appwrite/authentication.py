from rest_framework.authentication import BaseAuthentication

from django_appwrite.utilities import get_appwrite_settings, extract_token, \
    get_appwrite_user_info, check_verification, get_or_create_django_user


class AppwriteAuthentication(BaseAuthentication):
    def authenticate(self, request):
        appwrite_settings = get_appwrite_settings()
        token = extract_token(request, appwrite_settings)

        # Verify the token with Appwrite
        user_info = get_appwrite_user_info(token)

        # Check email and phone verification
        check_verification(user_info, appwrite_settings)

        # Authenticate or create Django user
        return get_or_create_django_user(request, user_info, appwrite_settings), token
