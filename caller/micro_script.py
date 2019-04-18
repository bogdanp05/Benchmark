import configparser
import os

import perf
import requests

LOCATION = os.path.abspath(os.path.dirname(__file__)) + '/'
config = configparser.ConfigParser()
config.read(LOCATION + '../config_micro.ini')

bm_info = configparser.ConfigParser()
bm_info.read(LOCATION + '../bm_info.ini')

APP_PATH = config['app']['protocol'] + '://' +\
           config['app']['url'] + ':' +\
           config['app']['port'] + '/'


def call_endpoint(endpoint):
    requests.get(APP_PATH + endpoint)


if __name__ == "__main__":
    values = config['run']['values']
    processes = config['run']['processes']
    runner = perf.Runner(values=values, processes=processes)
    runner.metadata['description'] = bm_info['bench']['desc']
    runner.bench_func(bm_info['bench']['name'], call_endpoint, bm_info['bench']['name'])
