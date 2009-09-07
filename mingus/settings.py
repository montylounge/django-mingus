import os, os.path, sys
from os.path import join, dirname, normpath
import re

PROJECT_ROOT = os.path.dirname(__file__)
MEDIA_ROOT = join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = join(MEDIA_ROOT, 'static')
STATIC_URL = '/media/static/'
ADMIN_MEDIA_PREFIX = '/admin_media/'

SITE_ID=1
ROOT_URLCONF = 'mingus.urls'
TIME_ZONE = 'America/New_York'
SECRET_KEY = '+bq@o(jph^-*sfj4j%xukecxb0jae9lci&ysy=609hj@(l$47c'
USE_I18N = False
HONEYPOT_FIELD_NAME = 'fonzie_kungfu'

MANAGERS = (
    ('fooper','your@emailaddress'),
)

TEMPLATE_DIRS = (
  [os.path.join(PROJECT_ROOT, "templates")]
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
'debug_toolbar.middleware.DebugToolbarMiddleware',
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
  'debug_toolbar',
  'contact_form',
  'honeypot',
  'sugar',
  'quoteme',
  'mingus',
)

try:
   from local_settings import *
except ImportError:
   pass


