from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import timedelta
import json
import sys
import environ

import pymysql
pymysql.install_as_MySQLdb()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECRET_KEY = 'django-insecure-q=!=((=y6#m54!yeqrslu-9c=(hfgya%93v0&li7l8g)n*mtxj'

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')
AUTH_USER_MODEL = 'accounts.User'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'accounts',
    'wish',
    'mypage',
    'alarms',

    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',

    'corsheaders'
]

SITE_ID = 2
# LOGIN_REDIRECT_URL = '/'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = (  # <-실제 요청에 허용되는 HTTP 동사 리스트
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'allauth.account.middleware.AccountMiddleware',
]

BASE_DIR = Path(__file__).resolve().parent.parent
REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',

    ),
}
REST_USE_JWT = True

SOCIALACCOUNT_PROVIDERS = {
    'kakao': {
        'SCOPE': ['account_email'],
        'AUTH_PARAMS': {'prompt': 'select_account'},
        'METHOD': 'oauth2',
        'VERSION': 'v2',
    }
}

ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # username 필드 사용 안함
ACCOUNT_EMAIL_REQUIRED = True  # email 필드 사용한다는 뜻
ACCOUNT_UNIQUE_EMAIL = True  # username 필드 사용 안함
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_LOGIN_ON_GET = True  # 중간 클릭 창 뜨지 않고 바로 넘어가게함
LOGIN_REDIRECT_URL = 'main'  # 로그인 완료후 연결될 url 설정함 (추후 변경)
ACCOUNT_LOGOUT_REDIRECT_URL = 'index'  # 로그아웃 후 연결될 url을 설정함
ACCOUNT_LOGOUT_ON_GET = True  # 로그아웃 요청시 바로 로그아웃 되도록 설정함

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

REST_USE_JWT = True
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'TOKEN_USER_CLASS': 'accounts.User',
}


# 이미지 관련 설정
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


ROOT_URLCONF = 'capstone.urls'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',

    'allauth.account.auth_backends.AuthenticationBackend',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'capstone.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ko-KR'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

load_dotenv()  # .env 파일 로드
KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")


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
