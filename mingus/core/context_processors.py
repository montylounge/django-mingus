from django.conf import settings
from basic.blog.models import Category
from django.core.cache import cache
from basic.blog.models import Settings
from basic.elsewhere.models import SocialNetworkProfile

def site_info(request):
    """
    Adds site-specific meta information to the context.
    
    To employ, add the site_info method reference to your project 
    settings TEMPLATE_CONTEXT_PROCESSORS.
    
    Example:
        TEMPLATE_CONTEXT_PROCESSORS = (
            ...
            "mingus.core.context_processors.site_info",
        )
    """
    
    site_id = settings.SITE_ID    
    key = 'basic.blog.settings:%s' % site_id
    blog_settings = cache.get(key, None)
    if blog_settings is None:
        blog_settings = Settings.get_current()
        cache.set(key, blog_settings)
        
    STATIC_URL = getattr(settings,'STATIC_URL', '')
        
    return {
        'BLOG_SETTINGS': blog_settings,
        'STATIC_URL': STATIC_URL,
    }