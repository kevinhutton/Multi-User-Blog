# Edit a given post

import webapp2
import time
import re
from models.like import Like
from models.post import Post
from misc.common import jinja_env,SecureCookie

class Editpost(webapp2.RequestHandler):

    # validate subject

    def validateSubject(self, subject):
        if subject == '':
            return False
        return True

    # validate content

    def validateContent(self, content):

        if content == '':
            return False
        return True
    # Edit post entity

    def editPost(self, post, subject, content):

        post.subject = subject
        post.content = content
        post.put()
        return post.key().id()

    # Display edit post form

    def get(self):

        # Make sure user is logged in and cookie is valid
        username = self.request.cookies.get('username')
        if not SecureCookie.verifySecureCookie(username) :
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(error="You must be logged in to view this page"))
            return

        currentUsername = SecureCookie.decryptSecureCookie(username)
        template = jinja_env.get_template('editpost.html')
        id = self.request.get('id')
        post = Post.get_by_id(int(id))
        # Only allow post-owner to edit post
        if currentUsername != post.username:
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(error="You are not the owner of the post, you cannot edit this post",currentUsername=currentUsername))
            return
        self.response.write(
            template.render(
                id=post.key().id(),
                subject=post.subject,
                content=post.content,
                currentUsername=currentUsername))

    # Handle edit post data

    def post(self):

        # Make sure user is logged in and cookie is valid
        username = self.request.cookies.get('username')
        if not SecureCookie.verifySecureCookie(username) :
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(error="You must be logged in to view this page"))
            return
        currentUsername = SecureCookie.decryptSecureCookie(username)
        id = self.request.get('id')
        post = Post.get_by_id(int(id))
        # Only allow post-owner to edit post
        if currentUsername != post.username:
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(error="You are not the owner of the post, you cannot edit this post",currentUsername=currentUsername))
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
            template = jinja_env.get_template('editpost.html')
            self.response.write(template.render(**errorMessages))
        else:
            key = self.editPost(post, subject, content)
            time.sleep(1)
            self.redirect('/%s' % key)