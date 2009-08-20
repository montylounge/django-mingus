from django.utils import simplejson
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from basic.blog.models import Post, Category
from django.conf import settings
from django import http
from django.template import loader, Context
from django_proxy.models import Proxy
from django.views.generic import list_detail
from django.core.cache import cache
from basic.blog.models import Settings
from view_cache_utils import cache_page_with_prefix
from contact_form.views import contact_form as django_contact_form
from contact_form.forms import ContactForm
from honeypot.decorators import check_honeypot

def page_key_prefix(request):
    return request.GET.get('page','')

def post_result_item(post):
    '''Generates the item result object for django-springsteen integration.'''
    return {
        'title': post.title,
        'url': settings.SITE_URL + post.get_absolute_url(),
        'text': post.body,
        }
        
def springsteen_results(request):
    '''
    Creates the django-springsteen compliant JSON results for only for findjango 
    integration.
    
    Results:
        Published Post objects.
    '''

    results = [ post_result_item(item) for item in Post.objects.published()[:50] ]
    response_dict = { 'total_results': Post.objects.published().count(), 'results': results, }
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    
    
def server_error(request, template_name='500.html'):
    '''Handles displaying 500 server error page along with application MEDIA.'''
    
    t = loader.get_template(template_name)
    return http.HttpResponseServerError(t.render(Context({
        "MEDIA_URL": settings.MEDIA_URL,
        "STATIC_URL": settings.STATIC_URL,
    })))


def springsteen_firehose(request):
    '''Generates django-springsteen compliant JSON results of proxy models for findjango integration.'''
    
    def result_item(proxy):
        '''Generates the item result object.'''
        
        if proxy.content_type.name == 'bookmark':
            url = proxy.content_object.get_absolute_url()
        else:
            url = settings.SITE_URL + proxy.content_object.get_absolute_url()
        
        return {
            'title': proxy.title,
            'url': url,
            'text': proxy.description,
            }
    
    posts = Proxy.objects.published()[:50].order_by('-pub_date')
    results = [ result_item(item) for item in posts ]
    response_dict = { 'total_results': Proxy.objects.published().count(), 'results': results, }
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    
def springsteen_category(request, slug):
    '''
    Creates the django-springsteen compliant JSON results for only for findjango 
    integration.
    
    Results:
        Published Post objects by category.
    '''
    
    category = get_object_or_404(Category, slug__iexact=slug)
    posts = category.post_set.published()[:50]
    results = [ post_result_item(item) for item in posts ]
    response_dict = { 'total_results': category.post_set.published().count(), 'results': results, }
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')


@cache_page_with_prefix(60, page_key_prefix)
def home_list(request, page=0, template_name='proxy/proxy_list.html', **kwargs):
    '''
    Homepage.
    
    Template: ``proxy/proxy_list.html``
    Context:
        object_list
            Aggregated list of Proxy instances (post, quote, bookmark).
        
    '''
        
    posts = Proxy.objects.published().order_by('-pub_date')    
    pagesize = Settings.get_current().page_size or 20
    
    return list_detail.object_list(
        request,
        queryset = posts,
        paginate_by = pagesize,
        page = page,
        template_name = template_name,
        **kwargs
    )
    
    
@check_honeypot
def contact_form(request, form_class=ContactForm,
                 template_name='contact_form/contact_form.html'):

    return django_contact_form(request, form_class=form_class,
                 template_name=template_name)
