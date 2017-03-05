import hmac
import random
import hashlib
import os
import re
import jinja2
from string import letters
from google.appengine.api import memcache
from google.appengine.ext import db
from post import Post
import logging


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = False)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

secret = 'mysupersecretwikikeythatnooneelseknowsexcpetthepeoplereadingmygithub'
def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())
    
def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val
        
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in range(length))
    
def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)
    
def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)
    
    
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)
    
PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)
    
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

def add_post(post, url):
    post.put()
    mc_set(key = url, val = post)
    return url

def get_post(url = ""):
    #mc_key = 'WIKI'
    post = mc_get(url)
    ##logging.info('UTILS: from MemCahce: ' + str(post_val))
    ##logging.info('UTILS: MemCache Values: ' + str(post[0]) + ', ' + m_url)
    #if post != None:
        #logging.info('UTILS: Found in MemeCache')
        #logging.info("UTILS: MemCache Value: " + str(post))
    #else:
        #logging.info('UTILS: Not Found in MemCache')

    if post is None:
        #logging.info('UTILS: fetching post from DB')
        results = Post.all().filter('url =', url).order('-created').fetch(1)
        #logging.info('UTILS: DB Results: ' + str(results))
        if len(results) == 0:
            mc_set(url, None)
            #logging.info('UTILS: Post Value: None')
        else:
            mc_set(url, results[0])
            #logging.info('UTILS: Post Value: ' + results[0].content)
            post = results[0]
    return post
    
def mc_get(key):
    return memcache.get(key)
    
def mc_set(key, val):
    if mc_get(key):
        memcache.replace(key, val)
        #logging.info('UTILS: replacing MemCache')
    else:
        #logging.info('UTILS: adding to MemCache')
        memcache.set(key, val)

def wiki_key(name = 'default'):
    return db.Key.from_path('wikis', name)