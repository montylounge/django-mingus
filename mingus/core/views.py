from django.utils import simplejson
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from basic.blog.models import Post, Category
from django.conf import settings
from django import http
from django.template import loader, Context
from django_proxy.models import Proxy
from django.views.generic import list_detail
from basic.blog.models import Settings
from view_cache_utils import cache_page_with_prefix
from contact_form.views import contact_form as django_contact_form
from contact_form.forms import ContactForm
from honeypot.decorators import check_honeypot
from tagging.models import Tag, TaggedItem
from django.shortcuts import render_to_response
from django.template import RequestContext
import re
from django.db.models import Q

def page_key_prefix(request):
    '''Used by cache_page_with_prefix to create a cache key prefix.'''
    return request.GET.get('page','')


def build_url(domainname):
    '''Given a domain name (ex mywebsite.com) it returns the full url.'''
    return 'http://%s' % domainname


def post_result_item(post):
    '''Generates the item result object for django-springsteen integration.'''
    return {
        'title': post.title,
        'url': build_url(Settings.get_current().site.domain) + post.get_absolute_url(),
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
    response_dict = { 'total_results': Post.objects.published().count(),
                    'results': results, }
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')


def server_error(request, template_name='500.html'):
    '''Handles displaying 500 server error page along with application MEDIA.'''

    t = loader.get_template(template_name)
    blog_settings = Settings.get_current()

    return http.HttpResponseServerError(t.render(Context({
        "MEDIA_URL": settings.MEDIA_URL,
        "STATIC_URL": settings.STATIC_URL,
        "BLOG_SETTINGS": blog_settings,
    })))

def springsteen_firehose(request):
    '''
    Generates django-springsteen compliant JSON results of proxy models for
    findjango integration.

    '''

    def result_item(proxy):
        '''Generates the item result object.'''

        if proxy.content_type.name == 'bookmark':
            url = proxy.content_object.get_absolute_url()
        else:
            url = build_url(Settings.get_current().site.domain) + proxy.content_object.get_absolute_url()

        return {
            'title': proxy.title,
            'url': url,
            'text': proxy.description,
            }

    posts = Proxy.objects.published().order_by('-pub_date')[:50]
    results = [ result_item(item) for item in posts ]
    response_dict = { 'total_results': Proxy.objects.published().count(),
                    'results': results, }
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')

def springsteen_category(request, slug):
    '''
    Creates the django-springsteen compliant JSON results for only for
    findjango integration.

    Results:
        Published Post objects by category.
    '''

    category = get_object_or_404(Category, slug__iexact=slug)
    posts = category.post_set.published()[:50]
    results = [ post_result_item(item) for item in posts ]
    response_dict = { 'total_results': category.post_set.published().count(),
                    'results': results, }
    return HttpResponse(simplejson.dumps(response_dict),
                        mimetype='application/javascript')


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


def quote_list(request, template_name='quotes/quote_list.html', **kwargs):
    '''
    A basic cxample of overriding a reusable apps view to customize.

    Displays quote list view. No paging added, but can be on your own.
    '''

    from quoteme.views import quote_list
    favorite_jazz_album = getattr(settings, 'FAVORITE_JAZZ_ALBUM', 'Money Jungle')
    extra = {
        'favorite_jazz_album': favorite_jazz_album,
    }

    return quote_list(request, template_name=template_name, extra_context=extra, **kwargs)


def quote_detail(request, template_name='quotes/quote_detail.html', **kwargs):
    '''
    A basic cxample of overriding a reusable apps view to customize.

    Displays quote detail view.
    '''

    from quoteme.views import quote_detail
    favorite_food = getattr(settings, 'FAVORITE_FOOD', 'Pizza')
    extra = {
        'favorite_food': favorite_food,
    }

    return quote_detail(request, template_name=template_name,
                        extra_context=extra, **kwargs)


def oops(request):
    '''An view that exists soley to provide an example of using django-db-log.'''
    foo = 1/0


def tag_detail(request, slug, template_name='proxy/tag_detail.html', **kwargs):
    ''' Display objects for all content types supported: Post and Quotes.'''

    tag = get_object_or_404(Tag, name__iexact=slug)

    #below could be prettier
    results = []
    qs = Proxy.objects.published().filter(tags__icontains=tag.name).order_by('-pub_date')
    for item in qs:
        comma_delimited = (',' in item.tags)
        if comma_delimited:
            for t in item.tags.split(','):
                if t.strip(' ') == tag.name:
                    results.append(item)
        else:
            for t in item.tags.split(' '):
                if t.strip(' ') == tag.name:
                    results.append(item)

    return render_to_response(template_name,
                    {'tag': tag, 'object_list': results},
                    context_instance=RequestContext(request),
                    )

@check_honeypot
def contact_form(request, form_class=ContactForm,
                 template_name='contact_form/contact_form.html'):

    '''
    Handles the contact form view. Leverages django-contact-form.

    This is an example of overriding another reusable apps view. This particular
    view also contains a form. For this example we are just doing the basic
    implementation by wrapping the view function and simply passing the
    arguments along.

    This view is also leveraging another reusable app, django-honeypot. The
    decorator you see being applied is used to protect your app from spam.
    '''
    return django_contact_form(request, form_class=form_class,
                 template_name=template_name)


# Stop Words courtesy of http://www.dcs.gla.ac.uk/idom/ir_resources/linguistic_utils/stop_words
STOP_WORDS = r"""\b(a|about|above|across|after|afterwards|again|against|all|almost|alone|along|already|also|
although|always|am|among|amongst|amoungst|amount|an|and|another|any|anyhow|anyone|anything|anyway|anywhere|are|
around|as|at|back|be|became|because|become|becomes|becoming|been|before|beforehand|behind|being|below|beside|
besides|between|beyond|bill|both|bottom|but|by|call|can|cannot|cant|co|computer|con|could|couldnt|cry|de|describe|
detail|do|done|down|due|during|each|eg|eight|either|eleven|else|elsewhere|empty|enough|etc|even|ever|every|everyone|
everything|everywhere|except|few|fifteen|fify|fill|find|fire|first|five|for|former|formerly|forty|found|four|from|
front|full|further|get|give|go|had|has|hasnt|have|he|hence|her|here|hereafter|hereby|herein|hereupon|hers|herself|
him|himself|his|how|however|hundred|i|ie|if|in|inc|indeed|interest|into|is|it|its|itself|keep|last|latter|latterly|
least|less|ltd|made|many|may|me|meanwhile|might|mill|mine|more|moreover|most|mostly|move|much|must|my|myself|name|
namely|neither|never|nevertheless|next|nine|no|nobody|none|noone|nor|not|nothing|now|nowhere|of|off|often|on|once|
one|only|onto|or|other|others|otherwise|our|ours|ourselves|out|over|own|part|per|perhaps|please|put|rather|re|same|
see|seem|seemed|seeming|seems|serious|several|she|should|show|side|since|sincere|six|sixty|so|some|somehow|someone|
something|sometime|sometimes|somewhere|still|such|system|take|ten|than|that|the|their|them|themselves|then|thence|
there|thereafter|thereby|therefore|therein|thereupon|these|they|thick|thin|third|this|those|though|three|through|
throughout|thru|thus|to|together|too|top|toward|towards|twelve|twenty|two|un|under|until|up|upon|us|very|via|was|
we|well|were|what|whatever|when|whence|whenever|where|whereafter|whereas|whereby|wherein|whereupon|wherever|whether|
which|while|whither|who|whoever|whole|whom|whose|why|will|with|within|without|would|yet|you|your|yours|yourself|
yourselves)\b"""

def proxy_search(request, template_name='proxy/proxy_search.html'):
    """
    Search for proxy objects. 99.99 percent borrowed from basic-blog's search.

    This template will allow you to setup a simple search form that will try to return results based on
    given search strings. The queries will be put through a stop words filter to remove words like
    'the', 'a', or 'have' to help imporve the result set.

    Template: ``proxy/proxy_search.html``
    Context:
        object_list
            List of blog posts that match given search term(s).
        search_term
            Given search term.
    """
    context = {}
    if request.GET:
        stop_word_list = re.compile(STOP_WORDS, re.IGNORECASE)
        search_term = '%s' % request.GET['q']
        cleaned_search_term = stop_word_list.sub('', search_term)
        cleaned_search_term = cleaned_search_term.strip()
        if len(cleaned_search_term) != 0:
            post_list = Proxy.objects.filter(Q(title__icontains=cleaned_search_term) | Q(tags__icontains=cleaned_search_term) | Q(description__icontains=cleaned_search_term)).order_by('-pub_date')
            context = {'object_list': post_list, 'search_term':search_term}
        else:
            message = 'Search term was too vague. Please try again.'
            context = {'message':message}
    return render_to_response(template_name, context, context_instance=RequestContext(request))