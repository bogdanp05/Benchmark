import configparser
import datetime
import os
import shutil
import signal
import subprocess
import sys
import time

import perf
from performance.run import run_command
from performance.utils import temporary_file
from sqlalchemy import create_engine, MetaData, exc

from caller import config, LOCATION

APP_PATH = config.micro_protocol + '://' + config.micro_url + ':' + config.micro_port + '/'
APP_OUTPUT = LOCATION + '../output.log'
START_TIME = datetime.datetime.now().strftime("%y%m%d_%H:%M:%S")
RESULTS_DIR = LOCATION + '../results/micro/' + START_TIME
BENCHMARKS = config.benchmarks


def set_environment():
    os.environ["FLASK_APP"] = LOCATION + '../micro/app.py'
    os.environ["FMD_DB"] = config.micro_db_url
    os.environ["BM_SPEED"] = config.speed


def create_results_dir():
    os.mkdir(RESULTS_DIR)


def copy_config_file():
    shutil.copy2(LOCATION + '../config.ini', RESULTS_DIR)


def start_app(fmd_level, webserver):
    os.environ["FMD_LEVEL"] = str(fmd_level)
    command = []
    if webserver == 'werkzeug':
        command.extend(["flask", "run", "-p", config.micro_port])
    else:
        command.extend(["gunicorn", "-w", "1", "-b", config.micro_url + ':' + config.micro_port, "micro.app:app"])

    with open(APP_OUTPUT, 'a') as f:
        server_process = subprocess.Popen(command, stdout=f)
    return server_process.pid


def stop_app(server_pid):
    os.kill(server_pid, signal.SIGTERM)


def drop_tables():
    try:
        engine = create_engine(config.micro_db_url)
        meta = MetaData(bind=engine)
        meta.reflect()
        for tbl in reversed(meta.sorted_tables):
            engine.execute(tbl.delete())
    except exc.InternalError as e:
        print(e)
        sys.exit(1)


def run_perf_script(level):
    bm_path = LOCATION + 'run_benchmarks.py'
    cmd = list(["python"])
    cmd.append('-u')
    cmd.append(bm_path)

    benchmarks = []
    for b in BENCHMARKS:
        drop_tables()
        server_pid = start_app(level, config.micro_webserver)
        time.sleep(config.bm_cooldown)
        benchmark_file = configparser.ConfigParser()
        benchmark_file['bench'] = {'name': b[0], 'desc': b[1]}
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
    filename = RESULTS_DIR + '/' + str(monitor_level) + '.json'
    return filename


def main():
    set_environment()
    create_results_dir()
    copy_config_file()
    for level in config.micro_levels:
        print("FMD level %d" % level)
        suite = run_perf_script(level)
        suite.dump(get_file_name(level))


if __name__ == "__main__":
    main()
