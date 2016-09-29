# New Post handler
import webapp2
import time
from models.post import Post
from misc.common import jinja_env,SecureCookie
import time
import re


class Newpost(webapp2.RequestHandler):

    # Make sure subject is valid format (E.g. non-empty)
    def validateSubject(self, subject):
        if subject == '':
            return False
        return True

    # Make sure content is valid format (E.g. non-empty)
    def validateContent(self, content):

        if content == '':
            return False
        return True

    # Create Post entity
    def insertPost(self, subject, content, username):

        newpost = Post(subject=subject, content=content, username=username)
        newpost.put()
        return newpost.key().id()

    # Generate new post creation page
    def get(self):

        # Make sure user is logged in and cookie is valid
        username = self.request.cookies.get('username')
        if not SecureCookie.verifySecureCookie(username) :
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(error="You must be logged in to view this page"))
            return
        else:
            template = jinja_env.get_template('newpost.html')
            self.response.write(template.render())
            return

    # Handle new post creation data

    def post(self):

        # Make sure user is logged in and cookie is valid
        username = self.request.cookies.get('username')
        if not SecureCookie.verifySecureCookie(username) :
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(error="You must be logged in to view this page"))
            return

        subject = self.request.get('subject')
        content = self.request.get('content')

        errorMessages = {}
        errorFound = False

        if not self.validateSubject(subject):
            errorMessages['subjecterror'] = "Invalid Subject"
            errorFound = True
        if not self.validateContent(content):
            errorMessages['contenterror'] = "Invalid Content"
            errorFound = True

        if errorFound:
            template = jinja_env.get_template('newpost.html')
            self.response.write(template.render(**errorMessages))
            return

        else:
            # Create Post entity , sleep prior to displaying the posting
            # page due to Data Store Delay
            key = self.insertPost(subject, content, SecureCookie.decryptSecureCookie(username))
            time.sleep(1)
            self.redirect('/%s' % key)
