#Unlike post handler
import webapp2
from misc.common import jinja_env,SecureCookie
from models.post import Post
from models.like import Like
import re
import time

class Unlikepost(webapp2.RequestHandler):

    def deleteLike(self, like):

        like.delete()

    def post(self):

        # Make sure user is logged in and cookie is valid
        username = self.request.cookies.get('username')
        if not SecureCookie.verifySecureCookie(username) :
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(error="You must be logged in to view this page"))
            return
        currentUsername = SecureCookie.decryptSecureCookie(username)

        # Get post which is being liked
        postid = self.request.get('id')
        post = Post.get_by_id(int(postid))

        # Do not allow users to unlike their own post
        if currentUsername == post.username:
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(error="You are not allowed to unlike your own post!"))
            return
        # If the current user has liked the post before , proceed in deleting the like
        like = post.likes.filter("username =", currentUsername).get()
        if like and (currentUsername == like.username):
            key = self.deleteLike(like)
            time.sleep(1)
            self.redirect('/')
        else:
            # Do not do anything if the user has not liked the post before
            self.redirect('/')




