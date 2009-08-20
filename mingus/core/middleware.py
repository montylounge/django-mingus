from django.conf import settings
from django.http import *
from django.views.debug import technical_500_response
import sys

class UserBasedExceptionMiddleware(object):
    '''
    Displays Django debugging messaage based on active user's session.
    
    Requirement:
        Active user's' session must be an authenticated superuser, or make sure active 
        user's IP address is in INTERNAL_IPs for the error message to display. Otherwise
        user will receive the configured server response, which is normally a "friendly"
        500 server error page.
        
    Source: http://ericholscher.com/blog/2008/nov/15/debugging-django-production-environments/
    '''
    def process_exception(self, request, exception):
        if request.user.is_superuser or request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            return technical_500_response(request, *sys.exc_info())