from base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_ACCESS_KEY_ID = os.environ.get('AWS_SES_ACCESS_KEY_ID')
AWS_SES_SECRET_ACCESS_KEY = os.environ.get('AWS_SES_SECRET_ACCESS_KEY')
AWS_SES_REGION_NAME = os.environ.get('AWS_SES_REGION_NAME', 'us-east-1')
AWS_SES_REGION_ENDPOINT = os.environ.get(
    'AWS_SES_REGION_ENDPOINT', 'email.us-east-1.amazonaws.com')

SLACK_URL = (os.environ.get('SLACK_URL'), os.environ.get('SLACK_TOKEN'))
CHANGELOG_API_TOKEN = os.environ.get('CHANGELOG_API_TOKEN')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE_NAME'),
        'USER': os.environ.get('MYSQL_USER'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
        'HOST': os.environ.get('MYSQL_HOST'),
        'PORT': os.environ.get('MYSQL_PORT', '3306'),
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'hub-cache'
    }
}


DEBUG = False

ALLOWED_HOSTS = ['*']
