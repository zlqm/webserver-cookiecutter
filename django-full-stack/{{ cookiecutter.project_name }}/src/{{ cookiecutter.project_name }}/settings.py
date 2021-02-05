import os
from pathlib import Path

from p_config import Config, Converter
import yaml

with open(Path(__file__).resolve().parent.joinpath('logging.yaml')) as f:
    LOGGING = yaml.safe_load(f)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$(O"hL-n^I~_SJu[M#$*kODK=[%>;<#O.b#Ri|*bqcPDKR?w'


# load config from file or env
class Boolean(Converter):
    def __call__(self, value):
        if isinstance(value, str):
            return m.upper() == 'TRUE'
        return bool(value)


class MyConfig(Config):
    DEBUG = Boolean()


CONFIG = Config(
    debug=False,
    allowed_hosts=['127.0.0.1', 'localhost'],
    api_jwt_secret_key=SECRET_KEY,

)
CONFIG.load_env()
# common config
_default_config_file = BASE_DIR.joinpath('conf', 'django.yaml')
_config_file = CONFIG.get('DJANGO_CONFIG_FILE', _default_config_file)
if os.path.exists(_config_file):
    CONFIG.load_file(_config_file)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.DEBUG

ALLOWED_HOSTS = CONFIG.ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_django_api.jwt.middleware.AuthenticationMiddleware',  # jwt auth
]

ROOT_URLCONF = '{{ cookiecutter.project_name }}.urls'

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

WSGI_APPLICATION = '{{ cookiecutter.project_name }}.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# Celery Configuration Options
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# API Config
API_JWT_SECRET_KEY = CONFIG.API_JWT_SECRET_KEY
