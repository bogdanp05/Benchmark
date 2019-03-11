import configparser

from config.parser import parse_literal, parse_string, parse_list


class Config(object):
    def __init__(self):
        """
            Sets the default values for the project
        """
        # benchmark
        self.values = 5
        self.processes = 20
        self.app_warmup = 3

        # app
        self.levels = [-1, 0, 1, 2, 3]
        self.url = "127.0.0.1"
        self.port = "5000"
        self.protocol = "http"
        self.webserver = "gunicorn"

    def init_from(self, file=None):
        parser = configparser.RawConfigParser()
        parser.read(file)

        # parse 'benchmark'
        self.values = parse_literal(parser, 'benchmark', 'values', self.values)
        self.processes = parse_literal(parser, 'benchmark', 'processes', self.processes)
        self.app_warmup = parse_literal(parser, 'benchmark', 'app_warmup', self.app_warmup)

        # parse app
        self.levels = parse_list(parser, 'app', 'levels', self.levels)
        self.url = parse_string(parser, 'app', 'url', self.url)
        self.port = parse_string(parser, 'app', 'port', self.url)
        self.protocol = parse_string(parser, 'app', 'protocol', self.protocol)
        self.webserver = parse_string(parser, 'app', 'webserver', self.webserver)
