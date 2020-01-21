import configparser
import os

import pyperf
import subprocess

LOCATION = os.path.abspath(os.path.dirname(__file__)) + '/'
config = configparser.ConfigParser()
config.read(LOCATION + '../config_macro.ini')

bm_info = configparser.ConfigParser()
bm_info.read(LOCATION + '../bm_info.ini')

APP_PATH = config['app']['protocol'] + '://' +\
           config['app']['url'] + ':' +\
           config['app']['port'] + '/'


def invoke_locust(users):
    subprocess.run(['locust', '-f', LOCATION + '/locust.py',
                    '--host', APP_PATH, '--no-web', '-c', users, '-r', users])


if __name__ == "__main__":
    values = config['run']['values']
    processes = config['run']['processes']
    runner = perf.Runner(values=values, processes=processes)
    runner.metadata['description'] = "Macro benchmark using the Conduit application"
    runner.bench_func("macro", invoke_locust, bm_info['bench']['users'])
