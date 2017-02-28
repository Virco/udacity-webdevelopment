from handler import WikiHandler
import logging

class Logout(WikiHandler):
    
    def get(self):
        logging.info(self.request.path)
        self.logout()
        self.redirect('/')