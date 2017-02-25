from handler import WikiHandler

class WikiPage(WikiHandler):
    def get(self):
        self.write("WOO Code Organization is Working!!!")