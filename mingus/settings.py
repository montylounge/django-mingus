# -*- coding: utf-8 -*-

import logging
import os
import sys

DEBUG = False
TEMPLATE_DEBUG = False

PROJECT_ROOT        = os.path.dirname(__file__)
MEDIA_ROOT          = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL           = '/media/'
STATIC_ROOT         = os.path.join(MEDIA_ROOT, 'static')
STATIC_URL          = '/media/static/'
ADMIN_MEDIA_PREFIX  = '/admin_media/'

SITE_ID             = 1

INTERNAL_IPS        = ('127.0.0.1',)

ADMINS              = ()
MANAGERS            = ()

ROOT_URLCONF        = 'mingus.urls'

USE_I18N            = False
TIME_ZONE           = 'America/New_York'

# NOTE: You are strongly advised to change these values in local_settings.py:
SECRET_KEY          = '+bq@o(jph^-*sfj4j%xukecxb0jae9lci&ysy=609hj@(l$47c'
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
    'sugar.middleware.debugging.UserBasedExceptionMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'djangodblog.DBLogMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "basic.blog.context_processors.blog_settings",
    "mingus.core.context_processors.site_info",
    "navbar.context_processors.navbars",
)

INSTALLED_APPS = (
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
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
  'south',
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
  'mingus',
)

try:
    from local_settings import *
except ImportError, e:
    print >> sys.stderr, "Unable to import local_settings: continuing using development settings. Error: %s" % e

# n.b. This will have no effective if logging has already been configured in
# this process. If you want to change what logging does, set it in a place like
# local_settings.py or your WSGI app:

logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(levelname)s: %(message)s'
)

if DEBUG:
    try:
        import debug_toolbar
        INSTALLED_APPS += ('debug_toolbar',)
        MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    except ImportError:
        logging.warning("Running debug mode without debug_toolbar: install it if you need it")

