from handler import WikiHandler
from user import User
import utils
import logging

class Login(WikiHandler):
    def get(self):
        logging.info(self.request.path)
        if self.user:
            self.redirect('/')
        else:
            self.render('login-form.html')
        
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        
        u = User.login(username, password)
        
        if u:
            self.login(u)
            self.redirect(self.request.referer)
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)