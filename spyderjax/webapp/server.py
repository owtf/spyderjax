import urls
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options

import os

settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug" : True
}


class Server(object):
    def __init__(self):
        self.application = tornado.web.Application(
            handlers=urls.get_handlers(),
            template_path=settings["template_path"],
            debug=False,
            gzip=True,
            compiled_template_cache=False
            )
        self.server = tornado.httpserver.HTTPServer(self.application)

    def start(self):
        try:
            self.server.listen(9009)
            self.server.start()
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    s = Server()
    s.start()

