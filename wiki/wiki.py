from handler import WikiHandler
from user import User
from post import Post
from google.appengine.api import memcache
import logging

class WikiPage(WikiHandler):
    def get(self):
        post = get_post()
        self.render('wiki.html', post = post)
        logging.info(self.request.path)
        
    
        
def get_post(url = "", update = False,):
    mc_key = 'WIKI'
    post, url = mc_get(mc_key)
    if update or post is None:
        post = Post.all().filter('url =', url).order('-created').fetch(1)
        mc_set(mc_key, post, url)
    return post
    
def mc_get(key):
    r = memcache.get(key)
    if r:
        val, url = r
    else:
        val, url = None, ""
    return val, url
    
def mc_set(key, val, url):
    memcache.set(key, (val, url))
    