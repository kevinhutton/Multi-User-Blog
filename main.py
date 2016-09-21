#Imports

import webapp2
import os
import jinja2
import re
import time
import random
import hashlib
import string
import time
from google.appengine.ext import db

# Load jinja html templates

template_dir = os.path.join(os.path.dirname(__file__), 'templates' )
jinja_env = jinja2.Environment( loader = jinja2.FileSystemLoader(template_dir) , autoescape = True)


# Handler for Welcome page displayed after login or signup

class Welcome(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('welcome.html')
        username = self.request.cookies.get('username')
        if not username or not SecureCookie.verifySecureCookie(username):
            self.redirect('/signup')
        self.response.write(template.render(currentUsername=SecureCookie.decryptSecureCookie(username)))

# Class used to secure cookies with hash value so they can't be tampered with
class SecureCookie():

#Secret key used while encrypting cookie , salt should be 4 characters long

    secret = "secure"
    saltSize = 5

    @staticmethod
    def createSalt():

        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase) for x in range(Password.saltSize))

    @staticmethod
    def createSecureCookie(value):

        hashedValue = hashlib.sha256(SecureCookie.secret + str(value)).hexdigest()
        return "%s|%s" % (value,hashedValue)

    @staticmethod
    def decryptSecureCookie(cookieValue):

        if not cookieValue:
            return cookieValue
        value,hashedValue = cookieValue.split("|")
        return value

    @staticmethod
    def verifySecureCookie(cookieValue):
        if not cookieValue:
            return False
        value,hashedValue = cookieValue.split("|")
        if not (SecureCookie.createSecureCookie(value) == cookieValue):
            return False
        return True

# Class used to securely store encrypted passwords in User database/entity

class Password():

    secret = "secure"
    saltSize = 5

    @staticmethod
    def createSalt():

        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase) for x in range(Password.saltSize))

    @staticmethod
    def createPasswordHash(password,inputSalt=None):

        if inputSalt is None:
            inputSalt = Password.createSalt()
        hashPassword = hashlib.sha256(Password.secret + str(password) + str(inputSalt) ).hexdigest()
        return "%s|%s" % (hashPassword,inputSalt)

    @staticmethod
    def validPassword(password,actualPassword,salt):
        passwordHash = hashlib.sha256(Password.secret + password + salt).hexdigest()
        actualPasswordHash = hashlib.sha256(Password.secret + actualPassword + salt).hexdigest()
        return passwordHash == actualPasswordHash
# Signup page handler
#
class Signup(webapp2.RequestHandler):

    def createUser(self,username,password,email=None):

        passwordHash = Password.createPasswordHash(password,None)
        newuser = User(username=username,password=passwordHash,email=email)
        newuser.put()
        return newuser.key().id()

    def validateUsername(self,username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return USER_RE.match(username)

    def validatePasswords(self,password,verify):

        USER_RE = re.compile(r"^.{3,20}$")
        if USER_RE.match(password):
            if password == verify:
                return True
        return False

    def validateEmail(self,email):

        USER_RE = re.compile(r"[\S]+@[\S]+.[\S]+$")
        return USER_RE.match(email)

    def get(self):

        currentUsername = SecureCookie.decryptSecureCookie(self.request.cookies.get('username'))
        template = jinja_env.get_template('signup.html')
        self.response.write(template.render(currentUsername=currentUsername))

    def post(self):

        username = self.request.get('username')
        password = self.request.get('password')
        verify   = self.request.get('verify')
        email    = self.request.get('email')

        errorMessages = {}
        errorFound = False

        if not self.validateUsername(username):
            errorMessages['usernameerror'] = "Invalid Username"
            errorFound = True
        if User.all().filter("username =",username).get():
            errorMessages['usernameerror'] = "Username already exists !"
            errorFound = True

        if not self.validatePasswords(password,verify):
            errorMessages['passworderror'] = "Invalid Passwords"
            errorFound = True
        if email and not self.validateEmail(email):
            errorMessages['emailerror'] = "Invalid email"
            errorFound = True

        if errorFound:
            template = jinja_env.get_template('signup.html')
            self.response.write(template.render(**errorMessages))
        else:
            self.createUser(username,password,email)
            self.response.headers.add_header('Set-Cookie', 'username=%s; Path=/' % ( SecureCookie.createSecureCookie( str(username) ) ) )
            self.redirect('/')

#Login page

class Login(webapp2.RequestHandler):


    def validateUsername(self,username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return USER_RE.match(username)

    def validatePassword(self,password):

        USER_RE = re.compile(r"^.{3,20}$")
        if USER_RE.match(password):
            return True
        return False

    def get(self):
        currentUsername = SecureCookie.decryptSecureCookie(self.request.cookies.get('username'))
        template = jinja_env.get_template('login.html')
        self.response.write(template.render(currentUsername=currentUsername))
    def post(self):

        username =  self.request.get('username')
        password = self.request.get('password')
        errorMessages = {}
        errorFound = False

        if not self.validateUsername(username):
            errorMessages['usernameerror'] = "Invalid Username"
            errorFound = True
        if not self.validatePassword(password):
            errorMessages['passworderror'] = "Invalid Password"
            errorFound = True

        try:
            query = db.GqlQuery("SELECT * FROM User WHERE username='%s' " % username).get()
            passwordHash,salt = query.password.split("|")
            if not (Password.createPasswordHash(password,salt).split('|')[0] == passwordHash):
                errorMessages['passworderror'] = "Incorrect Password"
                errorFound = True
        except:
            errorMessages['passworderror'] = "Incorrect Username or Password"
            errorFound = True

        if errorFound:
            template = jinja_env.get_template('login.html')
            self.response.write(template.render(**errorMessages))
        else:
            self.response.headers.add_header('Set-Cookie', 'username=%s; Path=/' % (SecureCookie.createSecureCookie(str(username))))
            self.redirect('/welcome')

#Logout page

class Logout(webapp2.RequestHandler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'username=; Path=/')
        self.redirect('/')

# Create a new post

class Newpost(webapp2.RequestHandler):

    def validateSubject(self,subject):
        if subject == '' :
            return False;
        return True;

    def validateContent(self,content):

        if content == '' :
            return False;
        return True;

    def insertPost(self,subject,content,username):

        newpost = Post(subject=subject,content=content,username=username)
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
            username = SecureCookie.decryptSecureCookie(self.request.cookies.get('username'))
            if not username:
                self.redirect('/login')
            else:
                key = self.insertPost(subject,content,username)
                time.sleep(5)
                self.redirect('/%s' % key)
# Create a new comment for a given post

class Newcomment(webapp2.RequestHandler):


    def validateContent(self,content):

        if content == '' :
            return False;
        return True;

    def insertComment(self,post,content,username):

        newcomment = Comment(post=post,content=content,username=username)
        newcomment.put()
        return newcomment.key().id()

    def get(self):
        postid = self.request.get('id')
        currentUsername = SecureCookie.decryptSecureCookie(self.request.cookies.get('username'))
        template = jinja_env.get_template('newcomment.html')
        self.response.write(template.render(postid=postid,currentUsername=currentUsername))

    def post(self):

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
            username = SecureCookie.decryptSecureCookie(self.request.cookies.get('username'))
            if not username:
                self.redirect('/login')
            else:

                key = self.insertComment(post,content,username)
                time.sleep(1)
                self.redirect('/')


class Editcomment(webapp2.RequestHandler):


    def validateContent(self,content):

        if content == '' :
            return False;
        return True;

    def editComment(self,comment,content,username):

        comment.content = content
        comment.username = username
        comment.put()
        return comment.key().id()

    def get(self):

        commentid = self.request.get('commentid')
        comment = Comment.get_by_id(int(commentid))
        template = jinja_env.get_template('editcomment.html')
        self.response.write(template.render(commentid=commentid,content=comment.content))

    def post(self):

        commentid = self.request.get('commentid')
        content = self.request.get('content')
        errorMessages = {}
        errorFound = False

        comment = Comment.get_by_id(int(commentid))

        if not self.validateContent(content):
            errorMessages['contenterror'] = "Invalid Content"
            errorFound = True

        if errorFound:
            template = jinja_env.get_template('editcomment.html')
            self.response.write(template.render(**errorMessages))
        else:
            currentUsername = SecureCookie.decryptSecureCookie(self.request.cookies.get('username'))
            if not currentUsername:
                self.redirect('/login')
            elif currentUsername != comment.username:
                self.redirect('/login')
            else:

                key = self.editComment(comment,content,currentUsername)
                time.sleep(1)
                self.redirect('/')

# Edit a given post

class Editpost(webapp2.RequestHandler):

    def validateSubject(self,subject):
        if subject == '' :
            return False;
        return True;

    def validateContent(self,content):

        if content == '' :
            return False;
        return True;

    def editPost(self,id,subject,content):

        post = Post.get_by_id(int(id))
        post.subject = subject
        post.content = content
        post.put()
        return id

    def get(self):
        template = jinja_env.get_template('editpost.html')
        id = self.request.get('id')
        currentUsername = SecureCookie.decryptSecureCookie(self.request.cookies.get('username'))
        post = Post.get_by_id(int(id))
        self.response.write(template.render(id=post.key().id(),subject=post.subject,content=post.content,currentUsername=currentUsername))

    def post(self):

        id      =  self.request.get('id')
        subject =  self.request.get('subject')
        content =  self.request.get('content')

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
            key = self.editPost(id,subject,content)
            time.sleep(1)
            self.redirect('/%s' % key)

#Delete a given post

class Deletepost(webapp2.RequestHandler):

    def deletePost(self,post):
        post.delete()
        return id

    def post(self):

        postid      =  self.request.get('id')
        post = Post.get_by_id(int(postid))
        currentUsername = SecureCookie.decryptSecureCookie(self.request.cookies.get('username'))
        errorMessages = {}
        errorFound = False


        if post and currentUsername == post.username:
            key = self.deletePost(post)
        time.sleep(1)
        self.redirect('/')

# Delete a given comment

class Deletecomment(webapp2.RequestHandler):

    def deleteComment(self,comment):
        comment.delete()

    def post(self):

        commentid =  self.request.get('commentid')
        comment = Comment.get_by_id(int(commentid))
        currentUsername = SecureCookie.decryptSecureCookie(self.request.cookies.get('username'))
        errorMessages = {}
        errorFound = False

        if errorFound:
            template = jinja_env.get_template('editpost.html')
            self.response.write(template.render(**errorMessages))
        else:
            if currentUsername == comment.username:
                key = self.deleteComment(comment)
            time.sleep(1)
            self.redirect('/')

# Like a given post

class Likepost(webapp2.RequestHandler):

    def insertLike(self,post,username):

        like = Like(post=post,username=username)
        like.put()
        return like.key().id()

    def post(self):
        postid      =  self.request.get('id')
        post = Post.get_by_id(int(postid))
        currentUsername = SecureCookie.decryptSecureCookie(self.request.cookies.get('username'))
        like = post.likes.filter("username =",currentUsername).get()
        if not like and currentUsername and currentUsername != post.username :
            key = self.insertLike(post,currentUsername)
            time.sleep(1)
            self.redirect('/')
        elif not currentUsername :
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(errorMessage="You must be logged in to like a post"))
        elif currentUsername == post.username:
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(errorMessage="You cannot like your own post !"))
        else:
            self.redirect('/')


class Unlikepost(webapp2.RequestHandler):


    def deleteLike(self,like):

        like.delete()

    def post(self):

        postid      =  self.request.get('id')
        post = Post.get_by_id(int(postid))
        currentUsername = SecureCookie.decryptSecureCookie(self.request.cookies.get('username'))
        like = post.likes.filter("username =",currentUsername).get()
        if like and (currentUsername == like.username):
            key = self.deleteLike(like)
            time.sleep(1)
            self.redirect('/')
        elif not currentUsername:
            template = jinja_env.get_template('error.html')
            self.response.write(template.render(errorMessage="You must be logged in to delete a post"))
        else:
            self.redirect('/')


# Post Entity for Google App Engine Datastore (E.g. Our DB table)

class Post(db.Model):
    subject  = db.StringProperty(required = True)
    content  = db.TextProperty(required = True)
    created  = db.DateTimeProperty(auto_now_add = True)
    username = db.StringProperty(required = True)

class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.StringProperty()

class Comment(db.Model):
    post     = db.ReferenceProperty(Post, collection_name='comments')
    content  = db.TextProperty(required = True)
    created  = db.DateTimeProperty(auto_now_add = True)
    username = db.StringProperty(required = True)

class Like(db.Model):
    post = db.ReferenceProperty(Post, collection_name='likes')
    username = db.StringProperty(required = True)

# Main Page Handler

class MainPage(webapp2.RequestHandler):

    def get(self,id=None):
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

        if  currentUsernameCookie and SecureCookie.verifySecureCookie(currentUsernameCookie):
            currentUsername = SecureCookie.decryptSecureCookie(currentUsernameCookie)
        else:
            currentUsername = None
        numberOfLikes = Like.all(keys_only=True).count()

        self.response.write(template.render(posts=posts,currentUsername=currentUsername,numberOfLikes=numberOfLikes))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/([0-9]+)', MainPage),
    ('/newpost',Newpost),
    ('/editpost',Editpost),
    ('/deletepost',Deletepost),
    ('/newcomment',Newcomment),
    ('/deletecomment',Deletecomment),
    ('/editcomment',Editcomment),
    ('/likepost', Likepost),
    ('/unlikepost', Unlikepost),
    ('/signup', Signup),
    ('/login', Login),
    ('/logout', Logout),
    ('/welcome', Welcome),

], debug=True)
