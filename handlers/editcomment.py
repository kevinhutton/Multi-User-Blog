# Edit a given comment
import webapp2
import time
import re
from models.comment import Comment
from models.post import Post
from misc.common import jinja_env,SecureCookie

class Editcomment(webapp2.RequestHandler):

    # Make sure content is valid format (E.g. non-empty)

    def validateContent(self, content):

        if content == '':
            return False
        return True

    # Edit comment entity

    def editComment(self, comment, content, username):

        comment.content = content
        comment.username = username
        comment.put()
        return comment.key().id()

    # Display comment edit form

    def get(self):

        # Make sure user is logged in and cookie is valid
        username = self.request.cookies.get('username')
        if not SecureCookie.verifySecureCookie(username) :
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(error="You must be logged in to view this page"))
            return

        commentid = self.request.get('commentid')
        comment = Comment.get_by_id(int(commentid))
        currentUsername = SecureCookie.decryptSecureCookie(username)

        # Only allow comment-owner to edit comment
        if currentUsername != comment.username:
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(error="You are not the owner of the comment, you cannot edit this comment"))
            return
        template = jinja_env.get_template('editcomment.html')
        self.response.write(
            template.render(
                commentid=commentid,
                content=comment.content))

    # Handle comment edit data

    def post(self):

        # Make sure user is logged in and cookie is valid
        username = self.request.cookies.get('username')
        if not SecureCookie.verifySecureCookie(username) :
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(error="You must be logged in to view this page"))
            return

        currentUsername = SecureCookie.decryptSecureCookie(username)
        commentid = self.request.get('commentid')
        content = self.request.get('content')
        errorMessages = {}
        errorFound = False
        comment = Comment.get_by_id(int(commentid))

        # Only allow comment-owner to edit comment
        if currentUsername != comment.username:
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(error="You are not the owner of the comment, you cannot edit this comment"))
            return

        if not self.validateContent(content):
            errorMessages['contenterror'] = "Invalid Content"
            errorFound = True

        if errorFound:
            template = jinja_env.get_template('editcomment.html')
            self.response.write(template.render(**errorMessages))
        else:
            key = self.editComment(comment, content, currentUsername)
            time.sleep(1)
            self.redirect('/')