import configparser

import requests
import perf
import os

LOCATION = os.path.abspath(os.path.dirname(__file__)) + '/'
config = configparser.ConfigParser()
config.read(LOCATION + '../config.ini')

APP_PATH = config['app']['protocol'] + '://' + config['app']['url'] + ':' + config['app']['port'] + '/'


def call_pi_digits():
    r = requests.get(APP_PATH + 'pidigits/')
    r.json()


def call_float():
    r = requests.get(APP_PATH + 'float/')
    r.json()


def call_json_loads():
    r = requests.get(APP_PATH + 'json_loads/')
    r.json()


def call_path_lib():
    r = requests.get(APP_PATH + 'path_lib/')
    r.json()


def call_sql_combined():
    r = requests.get(APP_PATH + 'sql_combined/')
    r.json()


def call_sql_writes():
    r = requests.get(APP_PATH + 'sql_writes/')
    r.json()


def call_sql_reads():
    r = requests.get(APP_PATH + 'sql_reads/')
    r.json()


if __name__ == "__main__":
    values = config['benchmark']['values']
    processes = config['benchmark']['processes']
    runner = perf.Runner(values=values, processes=processes)
    runner.metadata['description'] = "Compute digits of pi."
    runner.bench_func('pidigits', call_pi_digits)
    runner.metadata['description'] = "Float benchmark"
    runner.bench_func('float', call_float)
    runner.metadata['description'] = "Benchmark json.loads()"
    runner.bench_func('json_loads', call_json_loads)
    runner.metadata['description'] = "Test the performance of pathlib operations"
    runner.bench_func('pathlib', call_path_lib)
    runner.metadata['description'] = "SQLAlchemy combined benchmark using SQLite"
    runner.bench_func('sqlalchemy_combined', call_sql_combined)
    runner.metadata['description'] = "SQLAlchemy write benchmark using SQLite"
    runner.bench_func('sqlalchemy_writes', call_sql_writes)
    runner.metadata['description'] = "SQLAlchemy read benchmark using SQLite"
    runner.bench_func('sqlalchemy_reads', call_sql_reads)
