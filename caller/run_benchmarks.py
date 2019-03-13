import configparser

import requests
import perf
import os

LOCATION = os.path.abspath(os.path.dirname(__file__)) + '/'
config = configparser.ConfigParser()
config.read(LOCATION + '../config.ini')

APP_PATH = config['app']['protocol'] + '://' + config['app']['url'] + ':' + config['app']['port'] + '/'
# ENDPOINTS = [['pidigits', 'Compute digits of pi.'],
#              ['float', 'Float benchmark'],
#              ['json_loads', 'Benchmark json.loads()'],
#              ['path_lib', 'Test the performance of pathlib operations'],
#              ['sql_combined', 'SQLAlchemy combined benchmark using SQLite'],
#              ['sql_writes', 'SQLAlchemy write benchmark using SQLite'],
#              ['sql_reads', 'SQLAlchemy read benchmark using SQLite']]
ENDPOINTS = [['pidigits', 'Compute digits of pi.']]


def call_endpoint(endpoint):
    r = requests.get(APP_PATH + endpoint)
    r.json()


if __name__ == "__main__":
    values = config['benchmark']['values']
    processes = config['benchmark']['processes']
    runner = perf.Runner(values=values, processes=processes)
    for e in ENDPOINTS:
        runner.metadata['description'] = e[1]
        runner.bench_func(e[0], call_endpoint, e[0])
