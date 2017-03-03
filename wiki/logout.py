from handler import WikiHandler
import logging

class Logout(WikiHandler):
    
    def get(self):
        logging.info(self.request.path)
        self.logout()
        cookie = self.read_secure_cookie('ref')  
        self.redirect(cookie) if cookie else self.redirect('/')
