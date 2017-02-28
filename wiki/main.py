import os
import utils
import webapp2
from wiki import WikiPage

PAGE_RE = '^[/]?[\S]+?$'

DEBUG = bool(os.environ['SERVER_SOFTWARE'].startswith('Development'))
app = webapp2.WSGIApplication([(PAGE_RE, WikiPage)], debug=DEBUG)
                                
# app = webapp2.WSGIApplication([('/signup', Signup), 
#                                 ('/login', Login), 
#                                 ('/logout', Logout), 
#                                 ('/_edit' + PAGE_RE, EditPage), 
#                                 (PAGE_RE, WikiPage), ], 
#                                 debug=DEBUG)



        
