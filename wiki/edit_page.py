from handler import WikiHandler
from user import User
from post import Post
import logging
import utils

class EditPage(WikiHandler):
    def get(self):
        path = self.getpath()
        #logging.info("Edit path is: " + self.request.path)

        if not self.user:
            self.redirect(path)
        
        self.set_secure_cookie('ref', path)
        #logging.info('EditPage: cookie set.')

        post = utils.get_post(path)
        #logging.info('EDIT: Content = ' + post.content)
        self.render('edit.html', post = post)
           
    def post(self):
        path = self.getpath()
        if not self.user:
            self.redirect(path)

        content = self.request.get('content')
        #logging.info('EDIT: content: ' + content)
        if content:
            p = Post(parent = utils.wiki_key(), content = content, url = path)
            #logging.info('EDIT: Post: ' + str(p))
            #logging.info('EDIT: Post.Url: ' + p.url)
            utils.add_post(post = p, url = path)
            self.redirect(path)
        
        
    def getpath(self):
        return self.request.path.replace('/_edit/', '/')