import utils
from google.appengine.ext import db

class Post(db.Model):
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    user = db.StringProperty(required = True)
    
    def render(self):
        self._render_text = self.content
        return utils.render_str("content.html", p = self)
        