# UI request handlers

import tornado.web
import collections

class UIhandler(tornado.web.RequestHandler):

    def reverse_url(self, name, *args):
        url = super(UIhandler, self).reverse_url(name, *args)
        url = url.replace('?','')
        return url.split('None')[0]

class Home(UIhandler):
    SUPPORTED_METHODS = ['GET']
    def get(self):
        self.render('index.html')
