# Comment Entity - Used to represent user comments
from google.appengine.ext import db
from models.post import Post

class Comment(db.Model):
    post = db.ReferenceProperty(Post, collection_name='comments')
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    username = db.StringProperty(required=True)