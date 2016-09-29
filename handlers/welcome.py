# Handler for Welcome page displayed after login or signup

import webapp2
from misc.common import jinja_env, SecureCookie


class Welcome(webapp2.RequestHandler):

    def get(self):

        # Make sure user is logged in and cookie is valid
        username = self.request.cookies.get('username')
        if not SecureCookie.verifySecureCookie(username):
            template = jinja_env.get_template('error.html')
            self.response.write(
                template.render(
                    error="You must be logged in to view this page"))
            return
        else:
            template = jinja_env.get_template('welcome.html')
            self.response.write(
                template.render(
                    currentUsername=SecureCookie.decryptSecureCookie(username)))
