import configparser
import os

import perf
import subprocess

LOCATION = os.path.abspath(os.path.dirname(__file__)) + '/'
config = configparser.ConfigParser()
config.read(LOCATION + '../config_macro.ini')

APP_PATH = config['app']['protocol'] + '://' +\
           config['app']['url'] + ':' +\
           config['app']['port'] + '/'


def invoke_locust():
    subprocess.run(['locust', '-f', LOCATION + '../locusts/my_locust.py',
                    '--host', APP_PATH, '--no-web', '-c', '1', '-r', '1'])


if __name__ == "__main__":
    values = config['run']['values']
    processes = config['run']['processes']
    runner = perf.Runner(values=values, processes=processes)
    runner.metadata['description'] = "Macro benchmark using the Conduit application"
    runner.bench_func("macro", invoke_locust)
