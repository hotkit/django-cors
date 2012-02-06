import logging
logger = logging.getLogger(__name__)

class FixIEContentType(object):
    def process_request(self, request):
        # we need to have request.META to begin with
        if not request.META:
            return

        if request.META.get('HTTP_USER_AGENT') and 'MSIE' in request.META.get('HTTP_USER_AGENT'):
            # this is IE calling
            if not request.META.get('HTTP_CONTENT_TYPE', request.META.get('CONTENT_TYPE', '')):
                request.META['HTTP_CONTENT_TYPE'] = 'text/plain'