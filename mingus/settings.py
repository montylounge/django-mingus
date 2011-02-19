# -*- coding: utf-8 -*-
import os

PROJECT_ROOT = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin_media/'

#staticfiles app values
STATIC_URL = '/media/mingus/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'media')
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'media', 'mingus'),
)

SITE_ID = 1
ROOT_URLCONF = 'mingus.urls'
TIME_ZONE = 'America/New_York'
SECRET_KEY = '+bq@o(jph^-*sfj4j%xukecxb0jae9lci&ysy=609hj@(l$47c'
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
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'slimmer.middleware.CompressHtmlMiddleware',
    'sugar.middleware.debugging.UserBasedExceptionMiddleware',
    'request.middleware.RequestMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "basic.blog.context_processors.blog_settings",
    "navbar.context_processors.navbars",
    "staticfiles.context_processors.static_url",
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

    # sentry requirements
    'indexer',
    'paging',
    'sentry',
    'sentry.client',

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

    'django_twitter',
    'django_bitly',
    'staticfiles',
    'tinymce',
    'django_wysiwyg',
    'cropper',
    'memcache_status',
    'request',
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

try:
    from local_settings import *
except ImportError:
    pass
