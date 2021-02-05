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
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
    ],
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        # 'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        #'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'simple_django_api.jwt.middleware.AuthenticationMiddleware',
    ],
    DATABASES=DATABASES,
    LANGUAGE_CODE='en-us',
    TIME_ZONE='UTC',
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
    API_JWT_SECRET_KEY='to-be-changed',
)

from django.core.wsgi import get_wsgi_application
from django.urls import path
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django_simple_api import jwt, permissions, views
from django_simple_api.webargs import use_args
from webargs import fields


class TokenView(views.APIView):
    @use_args({
        'username': fields.Str(required=True),
        'password': fields.Str(required=True),
    })
    def post(self, request, args):
        user = authenticate(username=args['username'],
                            password=args['password'])
        if user:
            return {'token': jwt.genereate_token(user)}
        else:
            return 'wrong username or password'


class ProfileView(views.APIView):
    method_perms = {'GET': permissions.LoginRequired}

    def get(self, request):
        return {'name': request.user.username}


urlpatterns = [
    path('tokens', TokenView.as_view()),
    path('profile', ProfileView.as_view()),
]

application = get_wsgi_application()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
