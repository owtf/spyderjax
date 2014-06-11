#!/usr/bin/python2
import tornado.web
import json


class Home(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class APIRequestHandler(tornado.web.RequestHandler):
    def write(self, chunk):
        if isinstance(chunk, list):
            super(APIRequestHandler, self).write(json.dumps(chunk))
            self.set_header("Content-Type", "application/json")
        else:
            super(APIRequestHandler, self).write(chunk)


class Help(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("help.html")

'''
class ConfigurationManager(UIRequestHandler):
    SUPPORTED_METHODS = ('GET')
    @tornado.web.asynchronous
    def get(self):
        self.render(
            "config_manager.html",
            configuration_api_url=self.reverse_url('configuration_api_url')
        )
'''
