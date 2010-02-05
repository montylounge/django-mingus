from django.db.models import signals
from django_proxy.signals import proxy_save, proxy_delete
from basic.blog.models import Post
from quoteme.models import Quote
from basic.bookmarks.models import Bookmark

signals.post_save.connect(proxy_save, Post, True)
signals.post_delete.connect(proxy_delete, Post)

signals.post_save.connect(proxy_save, Quote, True)
signals.post_delete.connect(proxy_delete, Quote)

signals.post_save.connect(proxy_save, Bookmark, True)
signals.post_delete.connect(proxy_delete, Bookmark)