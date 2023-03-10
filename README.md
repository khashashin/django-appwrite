# Appwrite Middleware for Django

![PyPI version](https://badge.fury.io/py/django-appwrite.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-appwrite)
![PyPI - License](https://img.shields.io/pypi/l/django-appwrite)

A Django middleware to authenticate users with Appwrite.

## Installation

To install `django_appwrite`, simply run:

```bash
$ pip install django-appwrite
```

## Usage
1. Add `django_appwrite` to your INSTALLED_APPS list in your Django project's `settings.py` file:

```python
INSTALLED_APPS = [
    ...,
    'django_appwrite',
    ...
]
```

2. Add `django_appwrite.middleware.AppwriteMiddleware` to your MIDDLEWARE list in your Django project's `settings.py` file. It should be placed after the `AuthenticationMiddleware`:

```python
MIDDLEWARE = [
    ...,
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_appwrite.middleware.AppwriteMiddleware',
    ...
]
```
3. Configure the Appwrite client settings in your Django settings file:
```python
APPWRITE = {
    'PROJECT_ENDPOINT': 'https://example.com/v1',
    'PROJECT_ID': 'PROJECT_ID',
    'PROJECT_API_KEY': 'PROJECT_API_KEY',
}
```
| Setting            | Default            | Description                                                                                                                                                                                                           |
|--------------------|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `PROJECT_ENDPOINT` |                    | The endpoint of your Appwrite project. You can find this in the Appwrite console under Settings > General.                                                                                                            |
| `PROJECT_ID`       |                    | The ID of your Appwrite project. You can find this in the Appwrite console under Settings > General.                                                                                                                  |
| `PROJECT_API_KEY`  |                    | The API key of your Appwrite project. You can find this in the Appwrite console under Settings > API Keys.                                                                                                            |
| `AUTH_HEADER`      | HTTP_AUTHORIZATION | The header name that will be used to get the JWT from the authorization header. The value of this header should be `Bearer [JWT]`                                                                                     |
| `USER_ID_HEADER`   | HTTP_USER_ID       | The header name that will be used to store the user ID.                                                                                                                                                               |
| `VERIFY_EMAIL`     | False              | If set to `True`, the middleware will check if the user's email address has been verified in Appwrite before authenticating the user. If the email address has not been verified, the user will not be authenticated. |
| `VERIFY_PHONE`     | False              | If set to `True`, the middleware will check if the user's phone number has been verified in Appwrite before authenticating the user. If the phone number has not been verified, the user will not be authenticated.   |

## How it works
This middleware class will get the user ID from the header specified in the `USER_ID_HEADER` setting.
It will then use this user ID to retrieve the user information from Appwrite using the `Users` service.
If a user is found, it will create a Django user if it doesn't exist, and authenticate the user.

Please note that this middleware is intended to be used in conjunction with the Appwrite client-side SDK to authorize users on the frontend, and does not provide any APIs for user authentication on its own.

## Example
This is an example of how you can configure your frontend to use this middleware. Note that this example uses the [axios](https://axios-http.com/) library.

```javascript
// axios interceptor to add the user ID to the request header
import axios from 'axios';
import { Client, Account } from 'appwrite';

const client = new Client()
    .setEndpoint('https://example.com/v1')
    .setProject('PROJECT_ID')
    .setKey('PROJECT_API_KEY');
    
const account = new Account(client);

axios.interceptors.request.use(async (config) => {
    // get the user_id and jwt from your auth service/provider
    const { user_id, jwt } = await yourAuthService();
    
    config.headers = {
        ...config.headers,
        Authorization: `Bearer ${jwt}`,
        'User-ID': user_id,
    }
    
    return config;
});
```

## License
The django-appwrite package is released under the MIT License. See the bundled [LICENSE](LICENSE) file for details.