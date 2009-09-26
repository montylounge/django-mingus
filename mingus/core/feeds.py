from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse

from basic.blog.models import Settings
from django_proxy.models import Proxy

class AllEntries(Feed):
    _settings = Settings.get_current()
    title = '%s all entries feed' % _settings.site_name
    description = 'All entries published and updated on %s' % _settings.site_name
    author_name = _settings.author_name
    copyright = _settings.copyright

    def link(self):
        return 'http://%s' % self._settings.site.domain

    def items(self):
        return Proxy.objects.published().order_by('-pub_date')[:10]

    def item_link(self, item):
        return item.content_object.get_absolute_url()

    def item_categories(self, item):
        return item.tags.replace(',', '').split()