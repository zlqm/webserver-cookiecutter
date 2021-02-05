import os
from pathlib import Path
import sys

from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').upper() == 'TRUE'
SECRET_KEY = '{{ cookiecutter.secret_key | replace("\'", "#")| replace("\\", "#") }}'
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.staticfiles',
    ],
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    DATABASES=DATABASES,
    LANGUAGE_CODE='en-us',
    TIME_ZONE='UTC',
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
)

from django.core.wsgi import get_wsgi_application
from django.urls import path
from django.http import HttpResponse


def index(request):
    return HttpResponse('hello world')


urlpatterns = [
    path('', index),
]

application = get_wsgi_application()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
