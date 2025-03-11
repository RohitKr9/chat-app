from django.utils.deprecation import MiddlewareMixin
from importlib import import_module
from django.conf import settings


class MyCustomSessionMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        super().__init__(get_response)
        engine = import_module(settings.SESSION_ENGINE)
        self.SessionStore = engine.SessionStore

    def process_request(self, request):
        session_key = request.headers.get('X-Session-Id')
        # if not session_key:
        #     session_key = request.POST('X-Session-Id')
        request.session = self.SessionStore(session_key)

        if not request.session.session_key:
            request.session.create()

    def process_response(self, request, response):
        session_key = request.session.session_key
        print(session_key, "this is test for session key")
        response.headers['X-Session-Id'] = session_key
        return response