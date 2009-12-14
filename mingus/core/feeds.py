from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse

from basic.blog.models import Settings
from django_proxy.models import Proxy

class AllEntries(Feed):
    _settings = None

    @property
    def settings(self):
        if self._settings is None:
            self._settings = Settings.get_current()
        return self._settings

    def title(self):
        return '%s all entries feed' % self.settings.site_name

    def description(self):
        return 'All entries published and updated on %s' % self.settings.site_name

    def author_name(self):
        return self.settings.author_name

    def copyright(self):
        return self.settings.copyright

    def link(self):
        return 'http://%s' % self._settings.site.domain

    def items(self):
        return Proxy.objects.published().order_by('-pub_date')[:10]

    def item_link(self, item):
        return item.content_object.get_absolute_url()

    def item_categories(self, item):
        return item.tags.replace(',', '').split()