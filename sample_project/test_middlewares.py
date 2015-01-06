from django import http
from django.test import TestCase
from django.test.utils import override_settings
from django_cors import middleware
import importlib


class TestXsSharingMiddleware(TestCase):
    def load_middleware(self):
        """
        need to do this because cors settings is loaded dynamically
        """
        importlib.reload(middleware)
        return middleware.XsSharingMiddleware()

    @override_settings(XS_SHARING_ALLOWED_ORIGINS='localhost:8080')
    def test_get_allowed_origin_is_string(self):
        middleware = self.load_middleware()
        request = http.HttpRequest()

        allowed_origin = middleware._get_allowed_origin(request)

        self.assertEqual(allowed_origin, 'localhost:8080')

    @override_settings(XS_SHARING_ALLOWED_ORIGINS=['localhost:8080', 'localhost:9090'])
    def test_get_allowed_origin_is_list(self):
        middleware = self.load_middleware()
        request = http.HttpRequest()
        request.META['HTTP_ORIGIN'] = 'localhost:9090'

        allowed_origin = middleware._get_allowed_origin(request)

        self.assertEqual(allowed_origin, 'localhost:9090')

    @override_settings(XS_SHARING_ALLOWED_ORIGINS=lambda request: request.META.get('HTTP_ORIGIN', '').split(':')[-1] in ['2555'])
    def test_get_allowed_origin_lambda_return_true(self):
        middleware = self.load_middleware()
        request = http.HttpRequest()
        request.META['HTTP_ORIGIN'] = 'localhost:2555'

        allowed_origin = middleware._get_allowed_origin(request)

        self.assertEqual(allowed_origin, 'localhost:2555')

    @override_settings(XS_SHARING_ALLOWED_ORIGINS=lambda request: request.META.get('HTTP_ORIGIN', '').split(':')[-1] in ['2555'])
    def test_get_allowed_origin_lambda_return_false(self):
        middleware = self.load_middleware()
        request = http.HttpRequest()
        request.META['HTTP_ORIGIN'] = 'localhost:9999'

        allowed_origin = middleware._get_allowed_origin(request)

        self.assertEqual(allowed_origin, '')

    @override_settings(XS_SHARING_ALLOWED_ORIGINS='localhost:8080')
    def test_process_request(self):
        middleware = self.load_middleware()
        request = http.HttpRequest()
        request.META['HTTP_ACCESS_CONTROL_REQUEST_METHOD'] = 'POST'

        response = middleware.process_request(request)
        self.assertEqual(response['Access-Control-Allow-Origin'], 'localhost:8080')
        self.assertEqual(response['Access-Control-Allow-Methods'], 'POST,GET,OPTIONS,PUT,DELETE')
        self.assertEqual(response['Access-Control-Allow-Credentials'], 'true')
        self.assertEqual(response['Access-Control-Allow-Headers'], 'X-Requested-With')

    @override_settings(XS_SHARING_ALLOWED_ORIGINS='localhost:8080')
    def test_process_response(self):
        middleware = self.load_middleware()
        request = http.HttpRequest()
        response = http.HttpResponse()

        response = middleware.process_response(request, response)
        self.assertEqual(response['Access-Control-Allow-Origin'], 'localhost:8080')
        self.assertEqual(response['Access-Control-Allow-Methods'], 'POST,GET,OPTIONS,PUT,DELETE')
        self.assertEqual(response['Access-Control-Allow-Credentials'], 'true')
        self.assertEqual(response['Access-Control-Allow-Headers'], 'X-Requested-With')
