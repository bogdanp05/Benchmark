import configparser
import datetime
import os
import signal
import subprocess
import time

import perf
from performance.run import run_command
from performance.utils import temporary_file

from caller import config, LOCATION

APP_PATH = config.protocol + '://' + config.url + ':' + config.port + '/'

APP_OUTPUT = LOCATION + '../output.log'
runner = perf.Runner()
START_TIME = datetime.datetime.now().strftime("%y%m%d_%H:%M:%S")

ENDPOINTS = [['pidigits', 'Compute digits of pi.'],
             ['float', 'Float benchmark']]


def set_flask_environment():
    os.environ["FLASK_APP"] = LOCATION + '../benchmark/app.py'
    print(os.environ["FLASK_APP"])


def start_app(fmd_level, webserver):
    os.environ["FMD_LEVEL"] = str(fmd_level)
    command = []
    if webserver == 'werkzeug':
        command.extend(["flask", "run", "-p", config.port])
    else:
        command.extend(["gunicorn", "-w", "1", "-b", config.url + ':' + config.port, "benchmark.app:app"])

    with open(APP_OUTPUT, 'a') as f:
        server_process = subprocess.Popen(command, stdout=f)
    time.sleep(config.app_warmup)
    return server_process.pid


def stop_app(server_pid):
    os.kill(server_pid, signal.SIGTERM)


def run_perf_script():
    bm_path = LOCATION + 'run_benchmarks.py'
    cmd = list(["python"])
    cmd.append('-u')
    cmd.append(bm_path)

    benchmarks = []
    for e in ENDPOINTS:
        benchmark_file = configparser.ConfigParser()
        benchmark_file['bench'] = {'name': e[0], 'desc': e[1]}
        with open('example.ini', 'w') as configfile:
            benchmark_file.write(configfile)

        with temporary_file() as tmp:
            cmd.extend(('--output', tmp))
            print(cmd)
            run_command(cmd)
            benchmarks.append(perf.Benchmark.load(tmp))

    return perf.BenchmarkSuite(benchmarks)


def create_results_dir():
    os.mkdir(LOCATION + '../results/' + START_TIME)


def get_file_name(monitor_level):
    filename = LOCATION + '../results/' + START_TIME + '/' + str(monitor_level) + '.json'
    return filename


def main():
    set_flask_environment()
    create_results_dir()
    for level in config.levels:
        server_pid = start_app(level, config.webserver)
        suite = run_perf_script()
        suite.dump(get_file_name(level))
        stop_app(server_pid)


if __name__ == "__main__":
    main()
