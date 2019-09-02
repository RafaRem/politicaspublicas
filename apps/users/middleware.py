from django.conf import settings
from django.contrib import auth
from datetime import datetime, timedelta
import json

class AutoLogout:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if not request.user.is_authenticated:
            response = self.get_response(request)
            #Can't log out if not logged in
            return response

        try:
            if datetime.now() - datetime.strptime(request.session['last_touch'],'%Y-%m-%d %H:%M:%S.%f') > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
                auth.logout(request)
                del request.session['last_touch']
                return
        except KeyError:
            pass
        request.session['last_touch'] = str(datetime.now())
        response = self.get_response(request)
        return response