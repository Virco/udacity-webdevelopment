from handler import WikiHandler
from user import User
from post import Post
from google.appengine.api import memcache

class WikiPage(WikiHandler):
    def get(self):
        #post = get_post()
        #self.render('wiki.html', post = post)
        self.write("Im a Wiki!")
        
def get_post(update = False):
    mc_key = 'WIKI'
    post = mc_get(mc_key)
    return None
    
def mc_get(key):
    r = memcache.get(key)
    val = r if r else None
    return val
        
    