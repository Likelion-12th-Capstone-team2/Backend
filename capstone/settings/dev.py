from .base import *  # noqa

DEBUG = True
<<<<<<< HEAD
=======
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')
>>>>>>> 84fc09e359782ed2e2ad81cc518ecf46d659acdc

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
        "OPTIONS": {"charset": "utf8mb4"},
    }
}