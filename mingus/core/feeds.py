from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse

from basic.blog.models import Settings
from django_proxy.models import Proxy
from tagging.models import Tag, TaggedItem

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
        return 'http://%s' % self.settings.site.domain

    def items(self):
        return Proxy.objects.published().order_by('-pub_date')[:10]

    def item_link(self, item):
        return item.content_object.get_absolute_url()

    def item_categories(self, item):
        tags = item.tags
        # Avoid problems with empty/null values:
        if not tags:
            return list()
        else:
            return tags.replace(',', '').split()


class ByTag(AllEntries):
    
    @property
    def settings(self):
        if self._settings is None:
            self._settings = Settings.get_current()
        return self._settings
        

    def title(self):
        return '%s all entries feed' % self.settings.site_name

    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Tag.objects.get(name__exact=bits[0])

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return reverse('blog_tag_detail', kwargs={'slug':obj.name})

    def description(self, obj):
        return "Posts recently tagged as %s" % obj.name

    def item_link(self, item):
        return item.content_object.get_absolute_url()

    def items(self, obj):
        return Proxy.objects.published().filter(
            tags__icontains=obj.name
        ).order_by('-pub_date')[:10]
