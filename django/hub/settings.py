import os

from decouple import config, Csv

DEBUG = config('DEBUG', False, cast=bool)
TEMPLATE_DEBUG = DEBUG

BASE_PATH = os.path.join(
    os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
)


# to be overriden
CHANGELOG_API_TOKEN = config('CHANGELOG_API_TOKEN')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

DEFAULT_CHANGELOG_RECIPIENTS = ()

SOCIALACCOUNT_ADAPTER = 'accounts.allauth_adapter.HubAccountAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGOUT_ON_GET = True
LOGIN_EXEMPT_URLS = (
    r'^accounts/google/login/$',
    r'^accounts/google/login/callback/$',
    r'^static/',
)

LOGIN_REDIRECT_URL = '/'


RAISE_EXCEPTIONS = True

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
)

AUTH_USER_MODEL = 'accounts.Account'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)


SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations',
    'taggit': 'taggit.south_migrations',
}

THUMBNAIL_ALIASES = {
    '': {
        'project': {'size': (90, 90), 'crop': True},
        'person': {'size': (35, 35), 'crop': True},
        'person_large': {'size': (70, 70), 'crop': True},
    },
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv(), default='*')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = config('TIME_ZONE', 'America/Sao_Paulo')

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = config('LANGUAGE_CODE', 'pt-br')

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(BASE_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(os.path.dirname(BASE_PATH), 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_PATH, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = config('SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'accounts.middleware.LoginRequiredMiddleware',
)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(BASE_PATH, 'hub', 'templates'),
)

INSTALLED_APPS = (
    # django contribs
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'bootstrapform',
    'easy_thumbnails',
    'mptt',
    'taggit',
    'south',

    # project apps
    'core',
    'accounts',
    'news',
    'projects',
    'teams',
    'pr',
    'awards',

)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': (
                '%(levelname)s %(asctime)s %(module)s '
                '%(process)d %(thread)d %(message)s'
            )
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'hub_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_PATH, '..', '..', 'hub.log'),
            'maxBytes': 50 * 1024 * 1024,  # 50 MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'hub': {
            'handlers': ['hub_logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

DATABASES = {
    'default': {
        'ENGINE': config('DATABSE_ENGINE',
                         default='django.db.backends.sqlite3'),
        'NAME': config('DATABASE_NAME', default='temp.db'),
        'USER': config('DATABASE_USER', default=''),
        'PASSWORD': config('DATABASE_PASSWORD', default=''),
        'HOST': config('DATABASE_HOST', default=''),
        'PORT': config('DATABASE_PORT', default=''),
    }
}


CACHES = {
    'default': {
        'BACKEND': config(
            'DEFAULT_CACHE_BACKEND',
            default='django.core.cache.backends.locmem.LocMemCache'
        ),
        'LOCATION': config(
            'DEFAULT_CACHE_LOCATION',
            default='hub-cache'
        ),
    }
}


EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    'django.core.mail.backends.smtp.EmailBackend'
)

AWS_SES_ACCESS_KEY_ID = config('AWS_SES_ACCESS_KEY_ID')
AWS_SES_SECRET_ACCESS_KEY = config('AWS_SES_SECRET_ACCESS_KEY')
AWS_SES_REGION_NAME = config('AWS_SES_REGION_NAME', 'us-east-1')
AWS_SES_REGION_ENDPOINT = config('AWS_SES_REGION_ENDPOINT',
                                 default='email.us-east-1.amazonaws.com')
