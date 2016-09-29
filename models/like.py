# Like Entity - Used to represent user like data

from google.appengine.ext import db
from post import Post


class Like(db.Model):
    post = db.ReferenceProperty(Post, collection_name='likes')
    username = db.StringProperty(required=True)
