# Signup page handler

import webapp2
import re
from models.user import User
from misc.common import jinja_env, SecureCookie, Password


class Signup(webapp2.RequestHandler):

    # Create User Entity
    def createUser(self, username, password, email=None):

        passwordHash = Password.createPasswordHash(password, None)
        newuser = User(username=username, password=passwordHash, email=email)
        newuser.put()
        return newuser.key().id()

    # Make sure username is valid format
    def validateUsername(self, username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return USER_RE.match(username)

    # Make sure passwords are of valid format and that they match
    def validatePasswords(self, password, verify):

        USER_RE = re.compile(r"^.{3,20}$")
        if USER_RE.match(password):
            if password == verify:
                return True
        return False

    # Make sure email format is valid

    def validateEmail(self, email):

        USER_RE = re.compile(r"[\S]+@[\S]+.[\S]+$")
        return USER_RE.match(email)

    # Generate signup form for user to fill out
    def get(self):

        currentUsername = SecureCookie.decryptSecureCookie(
            self.request.cookies.get('username'))
        template = jinja_env.get_template('signup.html')
        self.response.write(template.render(currentUsername=currentUsername))

    # Handle user signup data and create user if data is valid
    def post(self):

        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        errorMessages = {}
        errorFound = False

        if not self.validateUsername(username):
            errorMessages['usernameerror'] = "Invalid Username"
            errorFound = True
        if User.all().filter("username =", username).get():
            errorMessages['usernameerror'] = "Username already exists !"
            errorFound = True

        if not self.validatePasswords(password, verify):
            errorMessages['passworderror'] = "Invalid Passwords"
            errorFound = True
        if email and not self.validateEmail(email):
            errorMessages['emailerror'] = "Invalid email"
            errorFound = True

        if errorFound:
            template = jinja_env.get_template('signup.html')
            self.response.write(template.render(**errorMessages))
        else:
            self.createUser(username, password, email)
            self.response.headers.add_header(
                'Set-Cookie', 'username=%s; Path=/' %
                (SecureCookie.createSecureCookie(
                    str(username))))
            self.redirect('/')
