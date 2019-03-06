import configparser

import requests
import perf
import os

LOCATION = os.path.abspath(os.path.dirname(__file__)) + '/'
config = configparser.ConfigParser()
config.read(LOCATION + '../config.ini')

BASE_URL = 'http://127.0.0.1:'
PORT = str(config['caller']['port'])
APP_PATH = BASE_URL + PORT + '/'


def pidigits():
    r = requests.get(APP_PATH + 'pidigits/')
    r.json()


if __name__ == "__main__":
    values = config['caller']['values']
    processes = config['caller']['processes']
    runner = perf.Runner(values=values, processes=processes)
    runner.metadata['description'] = "Compute digits of pi."
    runner.bench_func('pidigits', pidigits)
