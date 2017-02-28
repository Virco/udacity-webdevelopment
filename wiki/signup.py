from handler import WikiHandler
from user import User
import utils
import logging

class Signup(WikiHandler):
    def get(self):
        self.render('signup-form.html')
        
    def post(self):
        logging.info(self.request.path)
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')
        
        params = dict(username = self.username, email = self.email)
        
        if not utils.valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True
            
        if not utils.valid_password(self.password):
            params['error_password'] = "That's not a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_password'] = "Passwords didn't match."
            have_error = True
        
        if not utils.valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True
            
        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()
            
    def done(self, *a, **kw):
        raise NotImplementedError
        
class Register(Signup):
    def done(self):
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()
            self.login(u)
            self.redirect('/')
    