import os
import utils
import webapp2
from wiki import WikiPage
from signup import Register
from login import Login
from logout import Logout
from edit_page import EditPage

#PAGE_RE = '^[/]?[\S]+?$'
PAGE_RE = '^[/]?(?!.*favicon\.ico).*[\S]+?$'

DEBUG = bool(os.environ['SERVER_SOFTWARE'].startswith('Development'))
app = webapp2.WSGIApplication([('/signup', Register),
                                ('/login', Login),
                                ('/logout', Logout),
                                ('^/_edit/[\S]*?$', EditPage),
                                (PAGE_RE, WikiPage)
                                ], debug=DEBUG)
                                
# app = webapp2.WSGIApplication([('/signup', Signup), 
#                                 ('/login', Login), 
#                                 ('/logout', Logout), 
#                                 ('/_edit' + PAGE_RE, EditPage), 
#                                 (PAGE_RE, WikiPage), ], 
#                                 debug=DEBUG)
        
