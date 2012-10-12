# Django settings for empor project.
import os
DIRNAME = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Sam Liu', 'genxstylez@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', #or 'oracle'.
        'NAME': 'empor', # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '123',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Taipei'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-TW'


ugettext = lambda s: s # dummy ugettext function, as django's docs say

LANGUAGES = (
    ('zh-TW', ugettext('Trad. Chinese')),
    ('zh-CN', ugettext('Simp. Chinese')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(ROOT_PATH, '../../media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(ROOT_PATH, '../../asset/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/asset/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(ROOT_PATH, 'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^t^i$tsu3-d$v&amp;41(2)5mr+(h-dj)#(fs6_i48hwn@^$jj%k^#'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'djangoflash.middleware.FlashMiddleware',
)

ROOT_URLCONF = 'empor.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    'django.core.context_processors.request',
    'djangoflash.context_processors.flash',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'member.backends.FacebookBackend',
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'empor.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, 'templates'),
    os.path.join(ROOT_PATH, '../templates')     
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django_extensions',
    'django_crontab',
    'empor',
    'product',
    'cart',
    'order',
    'discount',
    'easy_thumbnails',
    'member',
    'storages',
    'staff',
    'service',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

FILE_UPLOAD_TEMP_DIR = '/tmp'

THUMBNAIL_ALIASES = {
    '': {
        'small': {'size': (75, 75), 'crop': 'scale'},
        'medium': {'size': (330, 330), 'crop': 'scale'},
        'large': {'size': (800, 800), 'crop': 'scale'}
    }
}

CRONJOBS = [
    ('* */1 * * *', 'cart.cron.clean_carts'),
    ('* */1 * * *', 'order.cron.clean_orders'),
]

SHIPPING_DEFAULT_COST = 100
SHIPPING_OVERSEAS_COST = 500
SHIPPING_FREE_ITEM_COUNT = 2
SHIPPING_FREE_MINIMUM_PURCHASE = None

AWS_ACCESS_KEY_ID = 'AKIAJVYZPH6EZHTV7JKQ' 
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'emportest'
AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False
AWS_HEADERS = {
    'Expires': 'Thu, 31 Dec 2020 23:59:59 GMT',
    'Cache-Control': 'max-age=99999',
}

THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

DEFAULT_FROM_EMAIL = 'EMPOR <webmaster@empor.com.tw>'
#EMAIL_HOST = 'localhost'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'webmaster@empor.com.tw'
EMAIL_HOST_PASSWORD = '53780722'
EMAIL_PORT = 587

AUTH_PROFILE_MODULE = 'member.UserProfile'

AWS_ACCESS_KEY_ID = 'AKIAJVYZPH6EZHTV7JKQ' 
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'emportest'
AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False
AWS_HEADERS = {
    'Expires': 'Thu, 31 Dec 2020 23:59:59 GMT',
    'Cache-Control': 'max-age=99999',
}

try:
    from local_settings import *
except ImportError:
    pass
