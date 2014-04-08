#!/usr/bin/env python2
# -*- coding: utf-8 -*-


class Proxy:

    def __init__(self, type, host, user=None, password=None, port):
        self.type = type
        self.host = host
        self.user = user
        self.password = password
        self.port = port

    def check_port():
        '''
        port number should be between 0 and 65535
        '''
        if self.port > 0 and self.port < 65535:
            return self.port
        else:
            print 'Enter a port between 0 and 65535'

    def pass_url():
        return str(self.type + '://'' + self.user + ':' + self.password + '@' + self.host + ':' + self.port)
