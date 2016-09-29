# main.py
import webapp2
from handlers.mainpage import MainPage
from handlers.newpost import Newpost
from handlers.editpost import Editpost
from handlers.deletepost import Deletepost
from handlers.newcomment import Newcomment
from handlers.deletecomment import Deletecomment
from handlers.editcomment import Editcomment
from handlers.likepost import Likepost
from handlers.unlikepost import Unlikepost
from handlers.signup import Signup
from handlers.login import Login
from handlers.logout import Logout
from handlers.welcome import Welcome


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/([0-9]+)', MainPage),
    ('/newpost', Newpost),
    ('/editpost', Editpost),
    ('/deletepost', Deletepost),
    ('/newcomment', Newcomment),
    ('/deletecomment', Deletecomment),
    ('/editcomment', Editcomment),
    ('/likepost', Likepost),
    ('/unlikepost', Unlikepost),
    ('/signup', Signup),
    ('/login', Login),
    ('/logout', Logout),
    ('/welcome', Welcome),

], debug=True)
