# Main page handler
import webapp2
from models.post import Post
from models.like import Like
from google.appengine.ext import db
from misc.common import jinja_env, SecureCookie
import re
import time

# Front/Main Page Handler


class MainPage(webapp2.RequestHandler):

    def get(self, id=None):
        # If id is specified in get request , display only that one post
        # Otherwise , display all posts
        posts = []
        if id:
            post = Post.get_by_id(int(id))
            posts.append(post)
        else:
            posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")

        # Load main page
        template = jinja_env.get_template('main.html')

        # Check if user is logged in
        currentUsernameCookie = self.request.cookies.get('username')

        # Verify that cookie has not been spoofed
        # If it has , set currentUsername cookie to empty

        if currentUsernameCookie and SecureCookie.verifySecureCookie(
                currentUsernameCookie):
            currentUsername = SecureCookie.decryptSecureCookie(
                currentUsernameCookie)
        else:
            currentUsername = None
        numberOfLikes = Like.all(keys_only=True).count()

        self.response.write(
            template.render(
                posts=posts,
                currentUsername=currentUsername,
                numberOfLikes=numberOfLikes))
