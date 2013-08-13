class FixIEContentType(object):
    def process_request(self, request):
        # we need to have request.META to begin with
        if not request.META:
            return

        if request.META.get('HTTP_USER_AGENT') and 'MSIE' in request.META.get('HTTP_USER_AGENT'):
            # this is IE calling
            if not request.META.get('HTTP_CONTENT_TYPE', request.META.get('CONTENT_TYPE', '')):
                request.META['HTTP_CONTENT_TYPE'] = 'text/plain'

import re

from django.utils.text import compress_string
from django.utils.cache import patch_vary_headers

from django import http

try:
    from django.conf import settings
    XS_SHARING_ALLOWED_ORIGINS = settings.XS_SHARING_ALLOWED_ORIGINS
    XS_SHARING_ALLOWED_METHODS = settings.XS_SHARING_ALLOWED_METHODS
    XS_SHARING_ALLOWED_HEADERS = settings.XS_SHARING_ALLOWED_HEADERS
except:
    XS_SHARING_ALLOWED_ORIGINS = '*'
    XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']
    XS_SHARING_ALLOWED_HEADERS = ['X-Requested-With']

XS_SHARING_ALLOW_CREDENTIALS = True

class XsSharingMiddleware(object):
    """
        This middleware allows cross-domain XHR using the html5 postMessage API.


        Access-Control-Allow-Origin: http://foo.example
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
    """
    def _get_allowed_origin(self, request):
        allowed_origin = XS_SHARING_ALLOWED_ORIGINS
        if XS_SHARING_ALLOWED_ORIGINS and isinstance(XS_SHARING_ALLOWED_ORIGINS, list):
            if request.get('HTTP_ORIGIN') and request.META['HTTP_ORIGIN'] in XS_SHARING_ALLOWED_ORIGINS:
                allowed_origin = request.META['HTTP_ORIGIN']
            else:
                # just return the first one because we won't allow the request anyway
                allowed_origin = XS_SHARING_ALLOWED_ORIGINS[0]
        return allowed_origin

    def process_request(self, request):

        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            allowed_origin = self._get_allowed_origin(request)
            response['Access-Control-Allow-Origin']  = allowed_origin
            response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )
            response['Access-Control-Allow-Credentials'] = str(XS_SHARING_ALLOW_CREDENTIALS).lower()
            response['Access-Control-Allow-Headers'] = ",".join( XS_SHARING_ALLOWED_HEADERS )
            return response

        return None

    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response

        allowed_origin = self._get_allowed_origin(request)
        response['Access-Control-Allow-Origin']  = allowed_origin
        response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )
        response['Access-Control-Allow-Credentials'] = str(XS_SHARING_ALLOW_CREDENTIALS).lower()
        response['Access-Control-Allow-Headers'] = ",".join( XS_SHARING_ALLOWED_HEADERS )

        return response

