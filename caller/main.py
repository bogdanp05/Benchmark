import os
import subprocess
import time

import requests

from caller.database.run import add_run
from caller import LOCATION


BASE_URL = 'http://127.0.0.1:'
PORT = '5000'
APP_PATH = BASE_URL + PORT + '/'
USERNAME = 'admin'
PASSWORD = 'admin'
WARM_UP = 5  # sets the number of seconds to wait after starting the server
APP_OUTPUT = LOCATION + '../output.log'


def set_flask_environment():
    os.environ["FLASK_APP"] = LOCATION + '../benchmark/app.py'
    print(os.environ["FLASK_APP"])


def start_benchmark_app(fmd_level):
    os.environ["FMD_LEVEL"] = str(fmd_level)
    with open(APP_OUTPUT, 'a') as f:
        subprocess.Popen(["flask", "run", "-p", PORT], stdout=f)
    time.sleep(WARM_UP)


def stop_benchmark():
    requests.post(APP_PATH + 'shutdown')


def main():
    set_flask_environment()
    for level in range(-1, 4):
        start_benchmark_app(level)
        for load in range(10, 15):
            r = requests.get(APP_PATH + 'powerset/' + str(load))
            print(r.json())
            add_run('powerset', load, r.json()['response_time'], level)
        stop_benchmark()


if __name__ == "__main__":
    main()
