# Basic Django Facebook login application

This is a basic Django application using facebook as the main authentication
method.

This application should be running in an externally accessible server, since
for the deauthorization callback Facebook needs to send a request to the server.

Features implemented:

- Login/logout
- User profile showing name and profile picture
- Deauthorization handling setting the user account to inactive

## Install dependencies

```
pipenv install
```

A `requirements.txt` files is also provided.

```
pip install -r requirements.txt
```

## Apply migrations

```
pipenv run fb_login_app/manage.py migrate
```

## Run application

```
DJANGO_DEBUG=True DJANGO_ALLOWED_HOSTS=".example.com" \
DJANGO_SECRET_KEY="my-django-secret" \
DJANGO_SOCIAL_AUTH_FACEBOOK_KEY="my-facebook-key" \
DJANGO_SOCIAL_AUTH_FACEBOOK_SECRET="my-facebook-secret" \
pipenv run gunicorn --chdir fb_login_app -w 3 fb_login_app.wsgi
```