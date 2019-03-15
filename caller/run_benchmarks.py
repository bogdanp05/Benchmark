import configparser
import os

import perf
import requests

LOCATION = os.path.abspath(os.path.dirname(__file__)) + '/'
config = configparser.ConfigParser()
config.read(LOCATION + '../config.ini')

config2 = configparser.ConfigParser()
config2.read(LOCATION + '../bm_info.ini')

APP_PATH = config['app']['protocol'] + '://' + config['app']['url'] + ':' + config['app']['port'] + '/'


def call_endpoint(endpoint):
    r = requests.get(APP_PATH + endpoint)
    r.json()


if __name__ == "__main__":
    values = config['benchmark']['values']
    processes = config['benchmark']['processes']
    runner = perf.Runner(values=values, processes=processes)
    runner.metadata['description'] = config2['bench']['desc']
    runner.bench_func(config2['bench']['name'], call_endpoint, config2['bench']['name'])
