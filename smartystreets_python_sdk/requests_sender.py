from requests import Session, Request
from .response import Response
import smartystreets_python_sdk as smarty


class RequestsSender:
    def __init__(self, max_timeout=10000):
        self.session = Session()
        self.max_timeout = max_timeout
        self.debug = None

    def send(self, smarty_request):
        request = build_request(smarty_request)
        prepped_request = self.session.prepare_request(request)
        if self.debug:
            print_request_data(prepped_request)

        try:
            response = self.session.send(prepped_request, timeout=self.max_timeout)
        except Exception as e:
            return Response(None, None, e)

        if self.debug:
            print_response_data(response)

        return build_smarty_response(response)


def build_request(smarty_request):
    request = Request(url=smarty_request.url_prefix, params=smarty_request.parameters)
    request.headers['User-Agent'] = "smartystreets (sdk:python@{})".format(smarty.__version__)
    request.headers['Content-Type'] = smarty_request.content_type
    if smarty_request.referer:
        request.headers['Referer'] = smarty_request.referer
    if smarty_request.payload:
        request.data = smarty_request.payload
        request.method = 'POST'
    else:
        request.method = 'GET'
    return request


def build_smarty_response(inner_response):
    return Response(inner_response.text, inner_response.status_code)


def print_request_data(request):
    print(request.method)
    print()
    print('URL: {}\r\n'.format(request.url))
    print('Headers:')
    for header in request.headers:
        print('  {}: {}'.format(header, request.headers[header]))
    print()
    print('Body: ')
    print('  {}\r\n'.format(request.body))


def print_response_data(response):
    print('****** Response ******\r\n')
    print(response.status_code)
    print()
    print(response.text)
    print('**********************\r\n')
