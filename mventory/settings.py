"""
Django settings for mventory project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os

import logging_loki

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('MVENTORY_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('MVENTORY_DEBUG') or False

ALLOWED_HOSTS = [os.getenv('MVENTORY_HOSTNAME')]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_prometheus',
    'rest_framework',
    'inventory.apps.InventoryConfig'
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware'
]

ROOT_URLCONF = 'mventory.urls'

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

WSGI_APPLICATION = 'mventory.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Get Database Settings from the Environment
db_engine_name = os.getenv('MVENTORY_DB_ENGINE') or "sqlite3"
DB_ENGINE = f"django_prometheus.db.backends.{db_engine_name}"

if db_engine_name == "sqlite3":
    DATABASES = {
        'default': {
            'ENGINE': 'django_prometheus.db.backends.sqlite3',
            'NAME': BASE_DIR / 'data/mventory.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': os.getenv('MVENTORY_DB_NAME'),
            'HOST': os.getenv('MVENTORY_DB_HOST'),
            'USER': os.getenv('MVENTORY_DB_USER'),
            'PASSWORD': os.getenv('MVENTORY_DB_PASSWORD'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.getenv("MVENTORY_STATIC_ROOT")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
            'TEST_REQUEST_DEFAULT_FORMAT': 'json'
            }

# Octopart
OCTOPART_API_KEY=os.getenv('MVENTORY_OCTOPART_API_KEY')
OCTOPART_API_ENDPOINT='https://octopart.com/api/v4/endpoint'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {'()': 'pythonjsonlogger.jsonlogger.JsonFormatter'},
        'standard': {
            'format': '%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [traceID=%(otelTraceID)s spanID=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'loki': {
            'level': 'INFO',
            'class': 'logging_loki.LokiHandler',
            'url': f"{os.getenv('MVENTORY_LOKI_HOST')}/loki/api/v1/push",
            'tags': {"app": "mventory", "env": "dev"},
            'version': "1",
            'formatter': 'json',
        },
    },
    'loggers': {
        'root': {
            'handlers': ['loki', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['loki', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['loki', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['loki', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['loki', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}
