# Delete a given comment

import webapp2
from misc.common import jinja_env,SecureCookie
from models.post import Post
from models.comment import Comment
import time
import re

class Deletecomment(webapp2.RequestHandler):

    # Remove comment entity
    def deleteComment(self, comment):
        comment.delete()

    def post(self):

        # Make sure user is logged in and cookie is valid
        username = self.request.cookies.get('username')
        if not SecureCookie.verifySecureCookie(username) :
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(error="You must be logged in to view this page"))
            return

        commentid = self.request.get('commentid')
        comment = Comment.get_by_id(int(commentid))
        currentUsername = SecureCookie.decryptSecureCookie(username)

        # Only allow deletion if comment owner is issuing delete
        if currentUsername != comment.username:
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(error="You are not the owner of this comment, you cannot delete this comment"))
            return
        else:
            key = self.deleteComment(comment)
            time.sleep(1)
            self.redirect('/')
