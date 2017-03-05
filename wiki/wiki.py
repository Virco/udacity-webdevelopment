from handler import WikiHandler
from user import User
from post import Post
import logging
import utils

class WikiPage(WikiHandler):
    def get(self):
        post = utils.get_post(self.request.path)

        # logging.info("WIKI: Post is: " + str(post))
        # logging.info('WIKI: content: ' + str(post[0].content))
       
        if self.user and post is None:
            self.redirect('/_edit' + self.request.path)
        else:
            self.set_secure_cookie('ref', self.request.path)
            self.render('wiki.html', post = post)
        
        logging.info("WIKI: path is: " + self.request.path)