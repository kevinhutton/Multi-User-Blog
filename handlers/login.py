# Login page handler

import webapp2
from misc.common import jinja_env, SecureCookie, Password
from google.appengine.ext import db
from models.user import User
import re


class Login(webapp2.RequestHandler):

    # Make sure username is valid format
    def validateUsername(self, username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return USER_RE.match(username)

    # Make sure passwords are of valid format and that they match
    def validatePassword(self, password):

        USER_RE = re.compile(r"^.{3,20}$")
        if USER_RE.match(password):
            return True
        return False
    # Generate Login Form

    def get(self):
        currentUsername = SecureCookie.decryptSecureCookie(
            self.request.cookies.get('username'))
        template = jinja_env.get_template('login.html')
        self.response.write(template.render(currentUsername=currentUsername))
    # Verify login data and create username cookie if data is valid

    def post(self):

        username = self.request.get('username')
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
            query = db.GqlQuery(
                "SELECT * FROM User WHERE username='%s' " %
                username).get()
            passwordHash, salt = query.password.split("|")
            if not (
                Password.createPasswordHash(
                    password,
                    salt).split('|')[0] == passwordHash):
                errorMessages['passworderror'] = "Incorrect Password"
                errorFound = True
        except:
            errorMessages['passworderror'] = "Incorrect Username or Password"
            errorFound = True

        if errorFound:
            template = jinja_env.get_template('login.html')
            self.response.write(template.render(**errorMessages))
        else:
            self.response.headers.add_header(
                'Set-Cookie', 'username=%s; Path=/' %
                (SecureCookie.createSecureCookie(
                    str(username))))
            self.redirect('/welcome')
