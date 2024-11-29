from .base import *  # noqa

<<<<<<< HEAD
DEBUG = True
=======
DEBUG = False
>>>>>>> 84fc09e359782ed2e2ad81cc518ecf46d659acdc
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
        'OPTIONS': {"charset": "utf8mb4"},
    }
<<<<<<< HEAD
}
=======
}
>>>>>>> 84fc09e359782ed2e2ad81cc518ecf46d659acdc
