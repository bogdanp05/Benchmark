import os
import time
import subprocess

import requests

from caller.database.run import add_run

BASE_URL = 'http://127.0.0.1:'
PORT = '5000'
PATH = BASE_URL + PORT + '/'
USERNAME = 'admin'
PASSWORD = 'admin'
WARM_UP = 4
APP_OUTPUT = '../output.log'


def set_flask_environment():
    os.environ["FLASK_APP"] = "../benchmark/app.py"


def start_benchmark_app(fmd_level):
    os.environ["FMD_LEVEL"] = str(fmd_level)
    with open(APP_OUTPUT, 'a') as f:
        subprocess.Popen(["flask", "run", "-p", PORT], stdout=f)
    time.sleep(WARM_UP)


def stop_benchmark():
    requests.post(PATH + 'shutdown')


def main():
    set_flask_environment()
    for level in range(-1, 4):
        start_benchmark_app(level)
        for load in range(15, 24):
            r = requests.get(PATH + 'powerset/'+str(load))
            print(r.json())
            add_run('powerset', load, r.json()['response_time'], level)
        stop_benchmark()


if __name__ == "__main__":
    main()
