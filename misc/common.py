import os
import jinja2
import random
import hashlib
import string


# Load jinja2 html templates , we only need to do this once for the whole application

template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)

# Store cookies with hash value so they can't be tampered with

class SecureCookie():

    # Secret key used while encrypting cookie , salt should be 5 characters

    secret = "secure"
    saltSize = 5

    # Create Salt (E.g. Random string)
    @staticmethod
    def createSalt():

        return ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase +
                string.ascii_lowercase) for x in range(
                Password.saltSize))

    # Create hash for given cookie value
    @staticmethod
    def createSecureCookie(value):

        hashedValue = hashlib.sha256(
            SecureCookie.secret +
            str(value)).hexdigest()
        return "%s|%s" % (value, hashedValue)

    # Return cookie value and omit hash of value
    @staticmethod
    def decryptSecureCookie(cookieValue):

        if not cookieValue:
            return cookieValue
        value, hashedValue = cookieValue.split("|")
        return value

    # verify a given cookie value and it's hash
    @staticmethod
    def verifySecureCookie(cookieValue):
        if not cookieValue:
            return False
        value, hashedValue = cookieValue.split("|")
        if not value  or not (SecureCookie.createSecureCookie(value) == cookieValue):
            return False
        return True

# Store encrypted passwords in User database/entity


class Password():

    secret = "secure"
    saltSize = 5

    # Create Salt (E.g. Random string)
    @staticmethod
    def createSalt():

        return ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase +
                string.ascii_lowercase) for x in range(
                Password.saltSize))

    # Encrypt given password
    @staticmethod
    def createPasswordHash(password, inputSalt=None):

        if inputSalt is None:
            inputSalt = Password.createSalt()
        hashPassword = hashlib.sha256(
            Password.secret +
            str(password) +
            str(inputSalt)).hexdigest()
        return "%s|%s" % (hashPassword, inputSalt)

    # Verify encrypted password is valid
    @staticmethod
    def validPassword(password, actualPassword, salt):
        passwordHash = hashlib.sha256(
            Password.secret + password + salt).hexdigest()
        actualPasswordHash = hashlib.sha256(
            Password.secret + actualPassword + salt).hexdigest()
        return passwordHash == actualPasswordHash

