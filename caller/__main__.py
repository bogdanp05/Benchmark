import datetime
import os
import subprocess
import time

import perf
import requests
from performance.run import run_command
from performance.utils import temporary_file

from caller import config, LOCATION

BASE_URL = 'http://127.0.0.1:'


PORT = str(config.port)
APP_PATH = BASE_URL + PORT + '/'
WARM_UP = 3  # sets the number of seconds to wait after starting the server

APP_OUTPUT = LOCATION + '../output.log'
runner = perf.Runner()
START_TIME = datetime.datetime.now().strftime("%y%m%d_%H:%M:%S")


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
    bm_path = LOCATION + 'run_benchmarks.py'
    cmd = list(["python"])
    cmd.append('-u')
    cmd.append(bm_path)

    with temporary_file() as tmp:
        cmd.extend(('--output', tmp))
        print(cmd)
        run_command(cmd)
        return perf.BenchmarkSuite.load(tmp)


def create_results_dir():
    os.mkdir(LOCATION + '../results/' + START_TIME)


def get_file_name(monitor_level):
    filename = LOCATION + '../results/' + START_TIME + '/' + str(monitor_level) + '.json'
    return filename


def main():
    set_flask_environment()
    create_results_dir()
    for level in config.levels:
        start_app(level)
        suite = run_perf_script()
        suite.dump(get_file_name(level))
        stop_app()


if __name__ == "__main__":
    main()
