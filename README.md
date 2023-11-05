# Appwrite Middleware and Authentication for Django

![PyPI version](https://badge.fury.io/py/django-appwrite.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-appwrite)
![PyPI - License](https://img.shields.io/pypi/l/django-appwrite)
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/khashashin)

A Django package to authenticate users with Appwrite using middleware and/or Django Rest Framework (DRF) authentication classes.

## Installation

To install `django_appwrite`, simply run:

```bash
$ pip install django-appwrite
```

## Usage
### Middleware
Add `django_appwrite.middleware.AppwriteMiddleware` to your `MIDDLEWARE` list in your Django project's `settings.py` file. It should be placed after the `AuthenticationMiddleware`:

```python
MIDDLEWARE = [
    ...,
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_appwrite.middleware.AppwriteMiddleware',
    ...
]
```
### Django Rest Framework Authentication
If you're using Django Rest Framework, you can use the `AppwriteAuthentication` class.
Add `django_appwrite.authentication.AppwriteAuthentication` to the `DEFAULT_AUTHENTICATION_CLASSES` in your `settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'django_appwrite.authentication.AppwriteAuthentication',
        ...
    ),
    ...
}
```
## Configuration
Configure the Appwrite client settings in your Django settings file:
```python
APPWRITE = {
    'PROJECT_ENDPOINT': 'https://example.com/v1',
    'PROJECT_ID': 'PROJECT_ID',
}
```
| Setting            | Default            | Description                                                                                                                                                                                                           |
|--------------------|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `PROJECT_ENDPOINT` |                    | The endpoint of your Appwrite project. You can find this in the Appwrite console under Settings > General.                                                                                                            |
| `PROJECT_ID`       |                    | The ID of your Appwrite project. You can find this in the Appwrite console under Settings > General.                                                                                                                  |
| `AUTH_HEADER`      | HTTP_AUTHORIZATION | The header name that will be used to get the JWT from the authorization header. The value of this header should be `Bearer [JWT]`                                                                                     |
| `VERIFY_EMAIL`     | False              | If set to `True`, the middleware will check if the user's email address has been verified in Appwrite before authenticating the user. If the email address has not been verified, the user will not be authenticated. |
| `VERIFY_PHONE`     | False              | If set to `True`, the middleware will check if the user's phone number has been verified in Appwrite before authenticating the user. If the phone number has not been verified, the user will not be authenticated.   |
| `PREFIX_EMAIL`     |                    | The prefix to use for the email address when checking if the user's email address has been verified. This is useful if you are integrating django_appwrite to existing projects that already have users.              |

## How it works
1. **Middleware:** This middleware class will authorize the user by checking the JWT in the Authorization header. The JWT is obtained from the Authorization header and is then sent to the Appwrite API to verify the JWT. If the JWT is valid, the user will be authenticated.
2. **Authentication Class:** When used with Django Rest Framework, the authentication class provides an additional way to authenticate users via Appwrite.

Please note that this middleware is intended to be used in conjunction with the Appwrite client-side SDK to authorize users on the frontend, and does not provide any APIs for user authentication on its own.

## Example
This is an example of how you can configure your frontend to use this middleware. Note that this example uses the [axios](https://axios-http.com/) library.

```javascript
// axios interceptor to add jwt to the request header
import axios from 'axios';
import { Client, Account } from 'appwrite';

const client = new Client()
    .setEndpoint('https://example.com/v1')
    .setProject('PROJECT_ID')
    
const account = new Account(client);

axios.interceptors.request.use(async (config) => {
    // get jwt from your auth service/provider
    const { jwt } = await yourAuthService();
    
    config.headers = {
        ...config.headers,
        Authorization: `Bearer ${jwt}`
    }
    
    return config;
});
```
## Important Note on CSRF Protection
When using the `AppwriteMiddleware`, be aware that Django's built-in CSRF protection will expect a CSRF token for any mutating HTTP methods (like POST, PUT, DELETE, etc.). If you're using Appwrite tokens for authentication with this middleware, you might encounter CSRF validation issues, since the CSRF token might not be present or validated.

If you're only using the Appwrite token for authentication, and you're confident about the origin protection measures of your front-end, you might consider exempting certain views from CSRF protection. However, do this with caution and ensure you understand the security implications. Always ensure that your application is protected against Cross-Site Request Forgery attacks.

You can exempt views from CSRF protection using the `@csrf_exempt` decorator or by using the `csrf_exempt` function on specific routes in your `urls.py`. However, these methods can leave your application vulnerable if used carelessly. Always prioritize the security of your application and its users.
## License
The django-appwrite package is released under the MIT License. See the bundled [LICENSE](LICENSE) file for details.
