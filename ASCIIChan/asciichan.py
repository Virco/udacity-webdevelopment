import os
import re
import sys
import urllib2
from urllib2 import URLError
from xml.dom import minidom
from string import letters

import jinja2
import webapp2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
        
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

def art_key(name = 'default'):
    return db.Key.from_path('arts', name)

IP_URL = "http://api.hostip.info/?ip="
#http://freegeoip.net/xml/68.71.173.254
def get_coords(ip):
    url = IP_URL + ip
    content = None
    
    try:
        content = urllib2.urlopen(url).read()
    except URLError:
        return
    
    if content:
        d = minidom.parseString(content)
        coords = d.getElementsByTagName("gml:coordinates")
        if coords and coords[0].childNode[0].nodeValue:
            lan, lat = coords[0].childNode[0].nodeValue.split(',')
            return db.GeoPt(lat, lan)

class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
    def render_front(self, error = '', title = '', art = ''):
        arts = db.GqlQuery("Select * "
                            "FROM Art "
                            "WHERE ANCESTOR IS :1 "
                            "ORDER BY created DESC "
                            "LIMIT 10", art_key())
        self.render('front.html', title = title, art = art, error = error, arts = arts)
        
    def get(self):
        self.write(repr(get_coords(self.request.remote_addr)))
        return self.render_front()
        
    def post(self):
        title = self.request.get('title')
        art = self.request.get('art')
        
        if title and art:
            p = Art(parent = art_key(), title = title, art = art)
            p.put()
            #look up the user's coordinates from their IP
            #if we have coordinates, add them to the art
            
            
            self.redirect('/')
        else:
            error = "we need both a title and some artwork!"
            self.render_front(error = error, title = title, art = art)
                
        
app = webapp2.WSGIApplication([('/', MainPage)], debug = True)