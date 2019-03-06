import configparser

from config.parser import parse_literal


class Config(object):
    def __init__(self):
        """
            Sets the default values for the project
        """
        # caller
        self.values = 5
        self.processes = 20
        self.levels = [-1, 0, 1, 2, 3]
        self.port = 5000

    def init_from(self, file=None):
        parser = configparser.RawConfigParser()
        parser.read(file)

        # parse 'caller'
        self.values = parse_literal(parser, 'caller', 'values', self.values)
        self.processes = parse_literal(parser, 'caller', 'processes', self.processes)
        self.levels = parse_literal(parser, 'caller', 'levels', self.processes)
        self.port = parse_literal(parser, 'caller', 'port', self.port)
