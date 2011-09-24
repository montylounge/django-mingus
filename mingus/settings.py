# -*- coding: utf-8 -*-
import os

PROJECT_ROOT = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

#staticfiles app values
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static', 'betweenconcepts'),
    os.path.join(PROJECT_ROOT, 'static', 'mingus'),
)

# Login paths
LOGIN_REDIRECT_URL = '/admin/'

SITE_ID = 1
ROOT_URLCONF = 'mingus.urls'
TIME_ZONE = 'America/Chicago'
USE_I18N = False
HONEYPOT_FIELD_NAME = 'fonzie_kungfu'

TEMPLATE_DIRS = (
  os.path.join(PROJECT_ROOT, "templates"),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'slimmer.middleware.CompressHtmlMiddleware',
    'sugar.middleware.debugging.UserBasedExceptionMiddleware',
    'request.middleware.RequestMiddleware',
    'djangodblog.DBLogMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "basic.blog.context_processors.blog_settings",
    "navbar.context_processors.navbars",
)

INSTALLED_APPS = (
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.markup',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'django.contrib.admin',
  'django.contrib.sitemaps',
  'django.contrib.flatpages',
  'django.contrib.redirects',

  'django_extensions',
  'tagging',
  'djangodblog',
  'disqus',
  'basic.inlines',
  'basic.blog',
  'basic.bookmarks',
  'basic.media',
  'oembed',
  'flatblocks',
  'dbtemplates',
  'navbar',
  'sorl.thumbnail',
  'template_utils',
  'django_proxy',

  'django_markup',
  'google_analytics',
  'robots',
  'basic.elsewhere',
  'compressor',
  'contact_form',
  'honeypot',
  'sugar',
  'quoteme',
  'mingus.core',
  'debug_toolbar',
  
  'tinymce',
  'django_wysiwyg',
  'cropper',
  'memcache_status',
  'request',
  
  'portfolio',
)


TINYMCE_JS_URL = STATIC_URL + 'js/tiny_mce/tiny_mce.js'
TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'theme_advanced_toolbar_location': "top",
}

DJANGO_WYSIWYG_MEDIA_URL = STATIC_URL + "js/ckeditor/"
DJANGO_WYSIWYG_FLAVOR = "ckeditor"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

try:
   from local_settings import *
except ImportError:
   pass
