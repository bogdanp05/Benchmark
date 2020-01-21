import configparser
import datetime
import os
import time

import pyperf
from pyperformance.run import run_command
from pyperformance.utils import temporary_file

from caller import utils, config_micro, LOCATION, MICRO_FILE


def set_environment(flask_app, fmd_db, bm_speed):
    os.environ["FLASK_APP"] = LOCATION + '../' + flask_app
    os.environ["FMD_DB"] = fmd_db
    os.environ["BM_SPEED"] = str(bm_speed)


def run_perf_script(level):
    cmd = utils.build_command('micro_script.py')

    benchmarks = []
    for b in config_micro.benchmarks:
        if config_micro.clear_db:
            utils.drop_tables(config_micro.db_url)
        server_pid = utils.start_app(level, config_micro.webserver, config_micro.port,
                                     config_micro.url, 'micro.app:app', output=config_micro.output)
        time.sleep(config_micro.bm_cooldown)
        benchmark_file = configparser.ConfigParser()
        benchmark_file['bench'] = {'name': b[0], 'desc': b[1]}
        with open('bm_info.ini', 'w') as configfile:
            benchmark_file.write(configfile)

        with temporary_file() as tmp:
            cmd.extend(('--output', tmp))
            run_command(cmd)
            benchmarks.append(perf.Benchmark.load(tmp))

        utils.stop_app(server_pid)
        time.sleep(config_micro.bm_cooldown)

    return pyperf.BenchmarkSuite(benchmarks)


def test():
    set_environment('micro/app.py', config_micro.db_url, 50)
    server_pid = utils.start_app(1, 'gunicorn', config_micro.port,
                                 config_micro.url, 'micro.app:app', log=True)
    print(server_pid)


def run():
    for speed in config_micro.speed:
        start_time = datetime.datetime.now().strftime("%y%m%d_%H:%M:%S")
        results_dir = LOCATION + '../results/micro/' + start_time
        set_environment('micro/app.py', config_micro.db_url, speed)
        utils.create_results_dir(results_dir, MICRO_FILE)
        for level in config_micro.levels:
            print("FMD level %d" % level)
            suite = run_perf_script(level)
            suite.dump(utils.get_file_name(results_dir, level))
