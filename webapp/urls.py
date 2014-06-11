import tornado.web
import handlers
from server import settings


def get_handlers():

    URLS = [
            tornado.web.url(r'/?$', handlers.Home, name='home_url'),
            tornado.web.url(r'/help/?', handlers.Help, name='help_url'),
            #tornado.web.url(r'/configuration/?$', handlers.ConfigurationHandler, name='configurationURL'),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': settings["static_path"]})
    ]

    return(URLS)
