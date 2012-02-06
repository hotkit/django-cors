import logging
logger = logging.getLogger(__name__)

class FixIEContentType(object):
    def process_request(self, request):
        if 'MSIE' in request.META.get('HTTP_USER_AGENT'):
            # this is IE calling
            if not self.request.META.get('HTTP_CONTENT_TYPE', self.request.META.get('CONTENT_TYPE', '')):
                request.META['HTTP_CONTENT_TYPE'] = 'text/plain'