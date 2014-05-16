import os
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options

import urls

TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates/'))


class InterfaceServer(object):
    def __init__(self, Core):
        self.application = tornado.web.Application(
                                                    handlers=urls.get_handlers(Core),  # To be added
                                                    template_path=TEMPLATE_DIR,
                                                    debug=False,
                                                    gzip=True,
                                                    compiled_template_cache=False
                                                  )
        self.application.Core = Core
        self.server = tornado.httpserver.HTTPServer(self.application)
        self.manager_cron = tornado.ioloop.PeriodicCallback(self.application.Core.WorkerManager.manage_workers, 2000)


    def start(self):
        try:
            self.server.bind(8000)
            tornado.options.parse_command_line(args=[""])
            self.server.start(1)
            self.manager_cron.start()
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            pass
