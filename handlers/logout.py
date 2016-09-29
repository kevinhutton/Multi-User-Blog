# Logout page handler

import webapp2

class Logout(webapp2.RequestHandler):

    # Delete username cookie
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'username=; Path=/')
        self.redirect('/')