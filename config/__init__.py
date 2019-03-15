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
        self.bm_cooldown = 10

        # app
        self.levels = [-1, 0, 1, 2, 3]
        self.url = "127.0.0.1"
        self.port = "5000"
        self.protocol = "http"
        self.webserver = "gunicorn"

    def init_from(self, file=None):
        config_parser = configparser.RawConfigParser()
        config_parser.read(file)

        # parse 'benchmark'
        self.values = parse_literal(config_parser, 'benchmark', 'values', self.values)
        self.processes = parse_literal(config_parser, 'benchmark', 'processes', self.processes)
        self.bm_cooldown = parse_literal(config_parser, 'benchmark', 'bm_cooldown', self.bm_cooldown)

        # parse app
        self.levels = parse_list(config_parser, 'app', 'levels', self.levels)
        self.url = parse_string(config_parser, 'app', 'url', self.url)
        self.port = parse_string(config_parser, 'app', 'port', self.url)
        self.protocol = parse_string(config_parser, 'app', 'protocol', self.protocol)
        self.webserver = parse_string(config_parser, 'app', 'webserver', self.webserver)
