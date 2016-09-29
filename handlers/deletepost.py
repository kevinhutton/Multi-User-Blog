# Delete a given post

import webapp2
from misc.common import jinja_env,SecureCookie
from models.post import Post
import time
import re

class Deletepost(webapp2.RequestHandler):

    # Remove post entity
    def deletePost(self, post):
        post.delete()
        return id

    def post(self):

        # Make sure user is logged in and cookie is valid
        username = self.request.cookies.get('username')
        if not SecureCookie.verifySecureCookie(username) :
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(error="You must be logged in to view this page"))
            return
        postid = self.request.get('id')
        post = Post.get_by_id(int(postid))
        currentUsername = SecureCookie.decryptSecureCookie(username)

        # Only allow deletion if post owner is issuing delete
        if currentUsername != post.username:
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(error="You are not the owner of this post, you cannot delete this post",currentUsername=currentUsername))
            return
        key = self.deletePost(post)
        time.sleep(1)
        self.redirect('/')