import os
import re
import hashlib
import random
import logging
import utils

from string import letters
from datetime import datetime, timedelta

import jinja2
import webapp2

from google.appengine.ext import db
from google.appengine.api import memcache

DEBUG = bool(os.environ['SERVER_SOFTWARE'].startswith('Development'))

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)
    
class WikiHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)
        
    def set_secure_cookie(self, name, val):
        cookie_val = utils.make_secure_val(val)
        self.response.headers.add_header('Set-Cookie', '%s=%s; PATH=/' % (name, cookie_val))
    
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and utils.check_secure_val(cookie_val)
        
    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))
        
    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; PATH=/')
        
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
        

app = webapp2.WSGIApplication([('/signup', Signup), ('/login', Login), ('/logout', Logout), ('/_edit' + PAGE_RE, EditPage), (PAGE_RE, WikiPage), ], debug=DEBUG)