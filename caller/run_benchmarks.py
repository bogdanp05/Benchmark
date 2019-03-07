import configparser

import requests
import perf
import os

LOCATION = os.path.abspath(os.path.dirname(__file__)) + '/'
config = configparser.ConfigParser()
config.read(LOCATION + '../config.ini')

APP_PATH = config['app']['protocol'] + '://' + config['app']['url'] + ':' + config['app']['port'] + '/'


def pidigits():
    r = requests.get(APP_PATH + 'pidigits/')
    r.json()


def my_float():
    r = requests.get(APP_PATH + 'float/')
    r.json()


if __name__ == "__main__":
    values = config['benchmark']['values']
    processes = config['benchmark']['processes']
    runner = perf.Runner(values=values, processes=processes)
    runner.metadata['description'] = "Compute digits of pi."
    runner.bench_func('pidigits', pidigits)
    runner.metadata['description'] = "Float benchmark"
    runner.bench_func('float', my_float)
