import configparser

from caller.config.parser import parse_literal, parse_string, parse_list, parse_benchmarks


class ConfigMicro(object):
    def __init__(self):
        """
            Sets the default values for the micro benchmarks
        """
        # run
        self.values = 5
        self.processes = 20
        self.bm_cooldown = 10
        self.speed = "fast"

        # app
        self.url = "127.0.0.1"
        self.port = "5000"
        self.protocol = "http"
        self.webserver = "gunicorn"

        # fmd
        self.levels = [-1, 0, 1, 2, 3]
        self.db_url = 'sqlite:///fmd.db'

        # benchmarks
        self.benchmarks = [('pidigits', 'Compute digits of pi.')]

    def init_from(self, file=None):
        config_parser = configparser.RawConfigParser()
        config_parser.read(file)

        # parse run
        self.values = parse_literal(config_parser, 'run', 'values', self.values)
        self.processes = parse_literal(config_parser, 'run', 'processes', self.processes)
        self.bm_cooldown = parse_literal(config_parser, 'run', 'bm_cooldown', self.bm_cooldown)
        self.speed = parse_string(config_parser, 'run', 'speed', self.speed)

        # parse app
        self.url = parse_string(config_parser, 'app', 'url', self.url)
        self.port = parse_string(config_parser, 'app', 'port', self.port)
        self.protocol = parse_string(config_parser, 'app', 'protocol', self.protocol)
        self.webserver = parse_string(config_parser, 'app', 'webserver', self.webserver)

        # parse fmd
        self.levels = parse_list(config_parser, 'fmd', 'levels', self.levels)
        self.db_url = parse_string(config_parser, 'fmd', 'db_url', self.db_url)

        # parse benchmarks
        self.benchmarks = parse_benchmarks(config_parser, 'benchmarks', self.benchmarks)


class ConfigMacro(object):
    def __init__(self):
        """
            Sets the default values for the macro benchmark
        """
        # app
        self.db = 'sqlite:///macro.db'
        self.url = "127.0.0.1"
        self.port = "5000"
        self.protocol = "http"
        self.webserver = "gunicorn"

    def init_from(self, file=None):
        config_parser = configparser.RawConfigParser()
        config_parser.read(file)

        # parse app
        self.db = parse_string(config_parser, 'app', 'db', self.db)
        self.url = parse_string(config_parser, 'app', 'url', self.url)
        self.port = parse_string(config_parser, 'app', 'port', self.port)
        self.protocol = parse_string(config_parser, 'app', 'protocol', self.protocol)
        self.webserver = parse_string(config_parser, 'app', 'webserver', self.webserver)
