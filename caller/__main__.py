import configparser
import datetime
import os
import signal
import subprocess
import time
import glob
import shutil

import perf
from performance.run import run_command
from performance.utils import temporary_file

from caller import config, LOCATION

APP_PATH = config.protocol + '://' + config.url + ':' + config.port + '/'
APP_OUTPUT = LOCATION + '../output.log'
START_TIME = datetime.datetime.now().strftime("%y%m%d_%H:%M:%S")
RESULTS_DIR = LOCATION + '../results/' + START_TIME
# ENDPOINTS = [['pidigits', 'Compute digits of pi.'],
#              ['float', 'Float benchmark'],
#              ['json_loads', 'Benchmark json.loads()'],
#              ['path_lib', 'Test the performance of pathlib operations'],
#              ['sql_combined', 'SQLAlchemy combined benchmark using SQLite'],
#              ['sql_writes', 'SQLAlchemy write benchmark using SQLite'],
#              ['sql_reads', 'SQLAlchemy read benchmark using SQLite']]
ENDPOINTS = [['pidigits', 'Compute digits of pi.'],
             ['float', 'Float benchmark']]


def set_flask_environment():
    os.environ["FLASK_APP"] = LOCATION + '../benchmark/app.py'
    print(os.environ["FLASK_APP"])


def create_results_dir():
    os.mkdir(RESULTS_DIR)


def copy_config_file():
    shutil.copy2(LOCATION + '../config.ini', RESULTS_DIR)


def start_app(fmd_level, webserver):
    os.environ["FMD_LEVEL"] = str(fmd_level)
    command = []
    if webserver == 'werkzeug':
        command.extend(["flask", "run", "-p", config.port])
    else:
        command.extend(["gunicorn", "-w", "1", "-b", config.url + ':' + config.port, "benchmark.app:app"])

    with open(APP_OUTPUT, 'a') as f:
        server_process = subprocess.Popen(command, stdout=f)
    return server_process.pid


def stop_app(server_pid):
    os.kill(server_pid, signal.SIGTERM)


def delete_databases():
    # TODO: for mysql I need a better script
    [os.remove(x) for x in glob.glob(LOCATION + "../*.db")]


def run_perf_script(level):
    bm_path = LOCATION + 'run_benchmarks.py'
    cmd = list(["python"])
    cmd.append('-u')
    cmd.append(bm_path)

    benchmarks = []
    for e in ENDPOINTS:
        delete_databases()
        server_pid = start_app(level, config.webserver)
        time.sleep(config.bm_cooldown)
        benchmark_file = configparser.ConfigParser()
        benchmark_file['bench'] = {'name': e[0], 'desc': e[1]}
        with open('bm_info.ini', 'w') as configfile:
            benchmark_file.write(configfile)

        with temporary_file() as tmp:
            cmd.extend(('--output', tmp))
            run_command(cmd)
            benchmarks.append(perf.Benchmark.load(tmp))

        stop_app(server_pid)
        time.sleep(config.bm_cooldown)

    return perf.BenchmarkSuite(benchmarks)


def get_file_name(monitor_level):
    filename = LOCATION + '../results/' + START_TIME + '/' + str(monitor_level) + '.json'
    return filename


def main():
    set_flask_environment()
    create_results_dir()
    copy_config_file()
    for level in config.levels:
        suite = run_perf_script(level)
        suite.dump(get_file_name(level))


if __name__ == "__main__":
    main()
