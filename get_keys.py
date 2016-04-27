#!/usr/bin/env python
import cherrypy
import os
import sys
import threading
import traceback
import webbrowser
import json

from base64 import b64encode
from fitbit.api import FitbitOauth2Client
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError, MissingTokenError
from requests_oauthlib import OAuth2Session


class OAuth2Server:
    def __init__(self, client_id, client_secret,
                 redirect_uri='http://localhost:8080/'):
        """ Initialize the FitbitOauth2Client """
        self.redirect_uri = redirect_uri
        self.success_html = """
            <h1>You are now authorized to access the Fitbit API!</h1>
            <br/><h3>You can close this window</h3>"""
        self.failure_html = """
            <h1>ERROR: %s</h1><br/><h3>You can close this window</h3>%s"""
        self.oauth = FitbitOauth2Client(client_id, client_secret)

    def browser_authorize(self):
        """
        Open a browser to the authorization url and spool up a CherryPy
        server to accept the response
        """
        url, _ = self.oauth.authorize_token_url(redirect_uri=self.redirect_uri)
        # Open the web browser in a new thread for command-line browser support
        threading.Timer(1, webbrowser.open, args=(url,)).start()
        cherrypy.quickstart(self)

    @cherrypy.expose
    def index(self, state, code=None, error=None):
        """
        Receive a Fitbit response containing a verification code. Use the code
        to fetch the access_token.
        """
        error = None
        if code:
            try:
                self.oauth.fetch_access_token(code, self.redirect_uri)
            except MissingTokenError:
                error = self._fmt_failure(
                    'Missing access token parameter.</br>Please check that '
                    'you are using the correct client_secret')
            except MismatchingStateError:
                error = self._fmt_failure('CSRF Warning! Mismatching state')
        else:
            error = self._fmt_failure('Unknown error while authenticating')
        # Use a thread to shutdown cherrypy so we can return HTML first
        self._shutdown_cherrypy()
        return error if error else self.success_html

    def _fmt_failure(self, message):
        tb = traceback.format_tb(sys.exc_info()[2])
        tb_html = '<pre>%s</pre>' % ('\n'.join(tb)) if tb else ''
        return self.failure_html % (message, tb_html)

    def _shutdown_cherrypy(self):
        """ Shutdown cherrypy in one second, if it's running """
        if cherrypy.engine.state == cherrypy.engine.states.STARTED:
            threading.Timer(1, cherrypy.engine.exit).start()


if __name__ == '__main__':

    if not (len(sys.argv) == 2):
        print("Usage: python get_keys.py key_file_name")
        print("   - FITBIT_CLIENT_ID and FITBIT_CLIENT_SECRET environment variables must be set")
        print("   - You should have a browser open and be logged into the fitbit account you want to access")
        print("   - access token and refresh token will be retrieved and stored in key_file_name")
        print("   - can be used even if key file exists to get a new refresh token")
        sys.exit(1)

    server = OAuth2Server(os.environ['FITBIT_CLIENT_ID'], os.environ['FITBIT_CLIENT_SECRET'])
    server.browser_authorize()

    json.dump(server.oauth.token, open(sys.argv[1], 'w'))
    # print('FULL RESULTS = %s' % server.oauth.token)
    # print('ACCESS_TOKEN = %s' % server.oauth.token['access_token'])
    # print('REFRESH_TOKEN = %s' % server.oauth.token['refresh_token'])
    print('Keys saved in {}'.format(sys.argv[1]))
