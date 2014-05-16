import tornado.web
import handlers


def get_handlers(Core):

    URLS = [
                tornado.web.URLSpec(r'/?$', handlers.Home, name='home'),
    ]
    return(URLS)
