import configparser

from caller.config.parser import parse_literal, parse_string, parse_list, parse_benchmarks


class Config(object):
    def __init__(self):
        """
            Sets the default values for the project
        """
        # run
        self.values = 5
        self.processes = 20
        self.bm_cooldown = 10
        self.speed = "normal"

        # app
        self.micro_url = "127.0.0.1"
        self.micro_port = "5000"
        self.micro_protocol = "http"
        self.micro_webserver = "gunicorn"

        # fmd
        self.micro_levels = [-1, 0, 1, 2, 3]
        self.micro_db_url = 'sqlite:///fmd.db'

        # benchmarks
        self.benchmarks = [('pidigits', 'Compute digits of pi.')]

    def init_from(self, file=None):
        config_parser = configparser.RawConfigParser()
        config_parser.read(file)

        # parse run
        self.values = parse_literal(config_parser, 'micro_run', 'values', self.values)
        self.processes = parse_literal(config_parser, 'micro_run', 'processes', self.processes)
        self.bm_cooldown = parse_literal(config_parser, 'micro_run', 'bm_cooldown', self.bm_cooldown)
        self.speed = parse_string(config_parser, 'micro_run', 'speed', self.speed)

        # parse app
        self.micro_url = parse_string(config_parser, 'micro_app', 'url', self.micro_url)
        self.micro_port = parse_string(config_parser, 'micro_app', 'port', self.micro_url)
        self.micro_protocol = parse_string(config_parser, 'micro_app', 'protocol', self.micro_protocol)
        self.micro_webserver = parse_string(config_parser, 'micro_app', 'webserver', self.micro_webserver)

        # parse fmd
        self.micro_levels = parse_list(config_parser, 'micro_fmd', 'levels', self.micro_levels)
        self.micro_db_url = parse_string(config_parser, 'micro_fmd', 'db_url', self.micro_db_url)

        # parse benchmarks
        self.benchmarks = parse_benchmarks(config_parser, 'micro_benchmarks', self.benchmarks)
