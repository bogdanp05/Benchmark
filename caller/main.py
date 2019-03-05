import os
import subprocess
import time

import perf
import requests

from performance.utils import temporary_file
from performance.run import run_command


BASE_URL = 'http://127.0.0.1:'
PORT = '5000'
APP_PATH = BASE_URL + PORT + '/'
USERNAME = 'admin'
PASSWORD = 'admin'
WARM_UP = 3  # sets the number of seconds to wait after starting the server
LOCATION = os.path.abspath(os.path.dirname(__file__)) + '/'
APP_OUTPUT = LOCATION + '../output.log'
runner = perf.Runner()


def set_flask_environment():
    os.environ["FLASK_APP"] = LOCATION + '../benchmark/app.py'
    print(os.environ["FLASK_APP"])


def start_app(fmd_level):
    os.environ["FMD_LEVEL"] = str(fmd_level)
    with open(APP_OUTPUT, 'a') as f:
        subprocess.Popen(["flask", "run", "-p", PORT], stdout=f)
    time.sleep(WARM_UP)


def pidigits():
    r = requests.get(APP_PATH + 'pidigits/')
    r.json()


def stop_app():
    requests.post(APP_PATH + 'shutdown')


def run_perf_script():
    bm_path = './run_benchmarks.py'
    cmd = list(["python"])
    cmd.append('-u')
    cmd.append(bm_path)

    with temporary_file() as tmp:
        cmd.extend(('--output', tmp))
        print(cmd)
        run_command(cmd)
        return perf.BenchmarkSuite.load(tmp)


def main():
    set_flask_environment()
    for level in range(-1, 4):
        start_app(level)
        run_perf_script()
        stop_app()


if __name__ == "__main__":
    main()
