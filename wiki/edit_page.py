from handler import WikiHandler
from user import User
from post import Post
import logging

class EditPage(WikiHandler):
    def get(self):
        logging.info("Edit path is: " + self.request.path)
        self.write("Edit path is: " + self.request.path)
