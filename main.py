
import webapp2
import os
import jinja2
import re
import time
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates' )
jinja_env = jinja2.Environment( loader = jinja2.FileSystemLoader(template_dir))

# New post handler

class Newpost(webapp2.RequestHandler):

    def validateSubject(self,subject):
        if subject == '' :
            return False;
        return True;

    def validateContent(self,content):

        if content == '' :
            return False;
        return True;

    def insertIntoDB(self,subject,content):

        newpost = Post(subject=subject,content=content)
        newpost.put()
        return newpost.key().id()

    def get(self):
        template = jinja_env.get_template('newpost.html')
        self.response.write(template.render())

    def post(self):

        subject =  self.request.get('subject')
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
        else:
            key = self.insertIntoDB(subject,content)

            time.sleep(5)
            self.redirect('/%s' % key)

# Post Entity for Google App Engine Datastore (E.g. Our DB table)

class Post(db.Model):
        subject = db.StringProperty(required = True)
        content = db.TextProperty(required = True)
        created = db.DateTimeProperty(auto_now_add = True)

# Main Page Handler

class MainPage(webapp2.RequestHandler):

    def get(self,id=None):

        posts = []
        if id:
            post = Post.get_by_id(int(id))
            posts.append(post)
        else:

            posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
        template = jinja_env.get_template('main.html')
        self.response.write(template.render(posts=posts))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/([0-9]+)', MainPage),
    ('/newpost',Newpost)
], debug=True)
