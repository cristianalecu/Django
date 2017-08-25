"""
Django settings for frobshop project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys
from oscar.defaults import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vxjq!y3yx)%8ko3m1oo7_amzy$zelrq(nzv3%n0t!%%w9k%aaf'

# Path helper
PROJECT_DIR = os.path.dirname(__file__)
location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)
PY3 = sys.version_info >= (3, 0)

USE_TZ = True

DEBUG = True
TEMPLATE_DEBUG = True
SQL_DEBUG = True

ALLOWED_HOSTS = ['192.168.1.67', 'cristianalecu.pythonanywhere.com']

ADMINS = (
    ('Cristian Alecu', 'cristian.alecu@gmail.com'),
)
EMAIL_SUBJECT_PREFIX = '[Oscar sandbox] '
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MANAGERS = ADMINS

# Application definition

from oscar import get_core_apps

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django_extensions',
    # Debug toolbar + extensions
    #'debug_toolbar',
    #'template_timings_panel',
    #'south',
    #'rosetta',          # For i18n testing
    'compressor',
    #'apps.gateway',     # For allowing dashboard access
    'widget_tweaks',
] + get_core_apps()

SITE_ID = 1

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'frobshop.urls'

from oscar import OSCAR_MAIN_TEMPLATE_DIR
TEMPLATE_DIRS = (
    location('templates'),
    OSCAR_MAIN_TEMPLATE_DIR,
)

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            OSCAR_MAIN_TEMPLATE_DIR
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                'django.contrib.messages.context_processors.messages',

                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
            ],
            # 'loaders': [
            #         'django.template.loaders.filesystem.Loader',
            #         'django.template.loaders.app_directories.Loader',
            #         # needed by django-treebeard for admin (and potentially other libs)
            #         'django.template.loaders.eggs.Loader',
            # ],
        },
    },
]



WSGI_APPLICATION = 'frobshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DjangoEcom',
        'USER': 'admin',
        'PASSWORD': 'go4admin',
        'HOST' : '',
        'PORT' : '',
        'ATOMIC_REQUESTS': True
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

# Includes all languages that have >50% coverage in Transifex
# Taken from Django's default setting for LANGUAGES
gettext_noop = lambda s: s
LANGUAGES = (
    ('en-us', gettext_noop('United States English')),
    ('it', gettext_noop('Italian')),
    ('fr', gettext_noop('French')),
    ('de', gettext_noop('German')),
    ('ro', gettext_noop('Romanian')),
)

ROSETTA_STORAGE_CLASS = 'rosetta.storage.SessionRosettaStorage'
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
ROSETTA_REQUIRES_AUTH = False

TIME_ZONE = 'Europe/Bucharest'

USE_I18N = True

USE_L10N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    location('static/'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = '/'
APPEND_SLASH = True

# Haystack settings
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

# =============
# Debug Toolbar
# =============

# Implicit setup can often lead to problems with circular imports, so we
# explicitly wire up the toolbar
# DEBUG_TOOLBAR_PATCH_SETTINGS = False
# DEBUG_TOOLBAR_PANELS = [
#     'debug_toolbar.panels.versions.VersionsPanel',
#     'debug_toolbar.panels.timer.TimerPanel',
#     'debug_toolbar.panels.settings.SettingsPanel',
#     'debug_toolbar.panels.headers.HeadersPanel',
#     'debug_toolbar.panels.request.RequestPanel',
#     'debug_toolbar.panels.sql.SQLPanel',
#     'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#     'debug_toolbar.panels.templates.TemplatesPanel',
#     'template_timings_panel.panels.TemplateTimings.TemplateTimings',
#     'debug_toolbar.panels.cache.CachePanel',
#     'debug_toolbar.panels.signals.SignalsPanel',
#     'debug_toolbar.panels.logging.LoggingPanel',
#     'debug_toolbar.panels.redirects.RedirectsPanel',
# ]
INTERNAL_IPS = ['127.0.0.1', '::1']

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'verbose': {
#             'format': '%(levelname)s %(asctime)s %(module)s %(message)s',
#         },
#         'simple': {
#             'format': '[%(asctime)s] %(message)s'
#         },
#     },
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse'
#         }
#     },
#     'handlers': {
#         'null': {
#             'level': 'DEBUG',
#             'class': 'django.utils.log.NullHandler',
#         },
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose'
#         },
#         'checkout_file': {
#             'level': 'INFO',
#             'class': 'oscar.core.logging.handlers.EnvFileHandler',
#             'filename': 'checkout.log',
#             'formatter': 'verbose'
#         },
#         'gateway_file': {
#             'level': 'INFO',
#             'class': 'oscar.core.logging.handlers.EnvFileHandler',
#             'filename': 'gateway.log',
#             'formatter': 'simple'
#         },
#         'error_file': {
#             'level': 'INFO',
#             'class': 'oscar.core.logging.handlers.EnvFileHandler',
#             'filename': 'errors.log',
#             'formatter': 'verbose'
#         },
#         'sorl_file': {
#             'level': 'INFO',
#             'class': 'oscar.core.logging.handlers.EnvFileHandler',
#             'filename': 'sorl.log',
#             'formatter': 'verbose'
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#             'filters': ['require_debug_false'],
#         },
#     },
#     'loggers': {
#         # Django loggers
#         'django': {
#             'handlers': ['null'],
#             'propagate': True,
#             'level': 'INFO',
#         },
#         'django.request': {
#             'handlers': ['mail_admins', 'error_file'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.db.backends': {
#             'handlers': ['null'],
#             'propagate': False,
#             'level': 'DEBUG',
#         },
#         # Oscar core loggers
#         'oscar.checkout': {
#             'handlers': ['console', 'checkout_file'],
#             'propagate': False,
#             'level': 'INFO',
#         },
#         'oscar.catalogue.import': {
#             'handlers': ['console'],
#             'propagate': False,
#             'level': 'INFO',
#         },
#         'oscar.alerts': {
#             'handlers': ['null'],
#             'propagate': False,
#             'level': 'INFO',
#         },
#         # Sandbox logging
#         'gateway': {
#             'handlers': ['gateway_file'],
#             'propagate': True,
#             'level': 'INFO',
#         },
#         # Third party
#         'south': {
#             'handlers': ['null'],
#             'propagate': True,
#             'level': 'INFO',
#         },
#         'sorl.thumbnail': {
#             'handlers': ['sorl_file'],
#             'propagate': True,
#             'level': 'INFO',
#         },
#         # Suppress output of this debug toolbar panel
#         'template_timings_panel': {
#             'handlers': ['null'],
#             'level': 'DEBUG',
#             'propagate': False,
#         }
#     }
# }

# Meta
# ====

OSCAR_SHOP_TAGLINE = 'Sandbox'

OSCAR_RECENTLY_VIEWED_PRODUCTS = 20
OSCAR_ALLOW_ANON_CHECKOUT = True

# This is added to each template context by the core context processor.  It is
# useful for test/stage/qa sites where you want to show the version of the site
# in the page title.
DISPLAY_VERSION = False


# Order processing
# ================

# Some sample order/line status settings
OSCAR_INITIAL_ORDER_STATUS = 'Pending'
OSCAR_INITIAL_LINE_STATUS = 'Pending'
OSCAR_ORDER_STATUS_PIPELINE = {
    'Pending': ('Being processed', 'Cancelled',),
    'Being processed': ('Processed', 'Cancelled',),
    'Cancelled': (),
    'Processed': (),
}


# LESS/CSS/statics
# ================

# We default to using CSS files, rather than the LESS files that generate them.
# If you want to develop Oscar's CSS, then set USE_LESS=True and
# COMPRESS_ENABLED=False in your settings_local module and ensure you have
# 'lessc' installed.  You can do this by running:
#
#    pip install -r requirements_less.txt
#
# which will install node.js and less in your virtualenv.

USE_LESS = False

COMPRESS_ENABLED = True
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)
COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': 'STATIC_URL',
    'use_less': USE_LESS,
}

# We do this to work around an issue in compressor where the LESS files are
# compiled but compression isn't enabled.  When this happens, the relative URL
# is wrong between the generated CSS file and other assets:
# https://github.com/jezdez/django_compressor/issues/226
COMPRESS_OUTPUT_DIR = 'oscar'

# Logging
# =======

LOG_ROOT = location('logs')
# Ensure log root exists
if not os.path.exists(LOG_ROOT):
    os.mkdir(LOG_ROOT)

# Sorl
# ====

THUMBNAIL_DEBUG = True
THUMBNAIL_KEY_PREFIX = 'oscar-sandbox'

# Use a custom KV store to handle integrity error
#THUMBNAIL_KVSTORE = 'oscar.sorl_kvstore.ConcurrentKVStore'

# Django 1.6 has switched to JSON serializing for security reasons, but it does not
# serialize Models. We should resolve this by extending the
# django/core/serializers/json.Serializer to have the `dumps` function. Also
# in tests/config.py
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Try and import local settings which can be used to override any of the above.
try:
    from settings_local import *
except ImportError:
    pass