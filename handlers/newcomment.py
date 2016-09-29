# New comment handler

import webapp2
import re
import time
from misc.common import jinja_env,SecureCookie
from models.comment import Comment
from models.post import Post


class Newcomment(webapp2.RequestHandler):

    # Make sure content is valid format (E.g. non-empty)

    def validateContent(self, content):

        if content == '':
            return False
        return True

    # Create comment entity
    def insertComment(self, post, content, username):

        newcomment = Comment(post=post, content=content, username=username)
        newcomment.put()
        return newcomment.key().id()
    # Display comment creation page

    def get(self):

        # Make sure user is logged in and cookie is valid
        username = self.request.cookies.get('username')
        if not SecureCookie.verifySecureCookie(username) :
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(error="You must be logged in to view this page"))
            return
        postid = self.request.get('id')
        currentUsername = SecureCookie.decryptSecureCookie(username)
        template = jinja_env.get_template('newcomment.html')
        self.response.write(
            template.render(
                postid=postid,
                currentUsername=currentUsername))
    # Handle comment creation data

    def post(self):

        # Make sure user is logged in and cookie is valid

        username = self.request.cookies.get('username')
        if not SecureCookie.verifySecureCookie(username) :
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(error="You must be logged in to view this page"))
            return
        postid = self.request.get('postid')
        content = self.request.get('content')
        errorMessages = {}
        errorFound = False

        post = Post.get_by_id(int(postid))

        if not self.validateContent(content):
            errorMessages['contenterror'] = "Invalid Content"
            errorFound = True

        if errorFound:
            template = jinja_env.get_template('newcomment.html')
            self.response.write(template.render(**errorMessages))
        else:
                # Create comment entity , sleep prior to displaying the posting
                # page due to data store delay
                key = self.insertComment(post, content, SecureCookie.decryptSecureCookie(username))
                time.sleep(1)
                self.redirect('/')

# Edit comment handler