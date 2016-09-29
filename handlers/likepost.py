
# Like a given post

import webapp2
from models.like import Like
from models.post import Post
from misc.common import jinja_env,SecureCookie
import time
import re

class Likepost(webapp2.RequestHandler):

    # Create Like entity

    def insertLike(self, post, username):

        like = Like(post=post, username=username)
        like.put()
        return like.key().id()

    # Increment Like counter

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
        # Do not allow users to like their own post
        if currentUsername == post.username:
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(error="You are not allowed to like your own post!"))
            return
        like = post.likes.filter("username =", currentUsername).get()

        # Do not allow users to like a post more than once
        if not like:
            key = self.insertLike(post, currentUsername)
            time.sleep(1)
            self.redirect('/')
        else:
            #Do nothing , just redirect if the user has already liked the post before
            self.redirect('/')
