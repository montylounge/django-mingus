from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.conf import settings
from basic.blog import views as blog_views
from basic.blog.feeds import BlogPostsFeed, BlogPostsByCategory
from basic.blog.sitemap import BlogSitemap
from mingus.core.views import springsteen_results, springsteen_firehose, \
                            home_list, springsteen_category, contact_form, \
                            proxy_search, oops, quote_list, quote_detail, \
                            tag_detail
from robots.views import rules_list
from mingus.core.feeds import AllEntries, ByTag

admin.autodiscover()

sitemaps = {
    'posts': BlogSitemap,
}

# override the default handler500 so we pass MEDIA_URL (nod to oebfare)
handler500 = "mingus.core.views.server_error"

urlpatterns = patterns('',
    url(r'^admin/password_reset/$',
        'django.contrib.auth.views.password_reset',
        name='password_reset'),
    (r'^password_reset/done/$',
     'django.contrib.auth.views.password_reset_done'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
     'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$',
     'django.contrib.auth.views.password_reset_complete'),

    (r'^admin/',
     include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^tinymce/',
     include('tinymce.urls')),

    url(r'^oops/$',
        oops,
        name='raise_exception'),

    url(r'^quotes/$',
        quote_list,
        name='quote_list'),

    url(r'^quotes/(?P<slug>[-\w]+)/$',
        quote_detail,
        name='quote_detail'),

    url(r'robots.txt$',
        rules_list,
        name='robots_rule_list'),

    (r'^sitemap.xml$',
     'django.contrib.sitemaps.views.sitemap',
     {'sitemaps': sitemaps}),

    #ex: /feeds/latest/
    url(r'^feeds/latest/$',
        BlogPostsFeed(),
        name='latest_feed'),

    #ex: /feeds/all/
    url(r'^feeds/all/$',
        AllEntries(),
        name='all_entries_feed'),

    #ex: /feeds/categories/django/
    url(r'^feeds/categories/(?P<slug>[-\w]+)/$',
        BlogPostsByCategory(),
        name='category_feed'),

    #ex: /feeds/tags/pony/
    url(r'^feeds/tags/(?P<name>[-\w]+)/$',
        ByTag(),
        name='tag_feed'),

    (r'^api/springsteen/posts/$',
     springsteen_results),
    (r'^api/springsteen/firehose/$',
     springsteen_firehose),
    (r'^api/springsteen/category/(?P<slug>[-\w]+)/$',
     springsteen_category),

    url(r'^contact/$',
        contact_form,
        name='contact_form'),

    url(r'^contact/sent/$',
        direct_to_template,
        { 'template': 'contact_form/contact_form_sent.html' },
        name='contact_form_sent'),

    url(r'^page/(?P<page>\w)/$',
        view=home_list,
        name='home_paginated'),

    url(r'^$',
        view=home_list,
        name='home_index'),

    url(r'^tags/(?P<slug>[-\w]+)/$',
        tag_detail,
        name='blog_tag_detail'),

    url (r'^search/$',
        view=proxy_search,
        name='proxy_search'),

    (r'',
     include('basic.blog.urls')),

    (r'^sentry/',
     include('sentry.urls')),
)


from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('', 
        (r'', include('staticfiles.urls')),
    )
