import configparser
import datetime
import os
import time

import pyperf
from pyperformance.run import run_command
from pyperformance.utils import temporary_file

from caller import utils, config_macro, LOCATION, MACRO_FILE

APP_PATH = config_macro.protocol + '://' +\
           config_macro.url + ':' +\
           config_macro.port + '/api'


def set_environment(flask_app):
    os.environ["FLASK_APP"] = LOCATION + '../' + flask_app
    os.environ["APP_DB"] = config_macro.app_db
    os.environ["FMD_DB"] = config_macro.fmd_db


def run_perf_script(level, user):
    cmd = utils.build_command('macro_script.py')

    benchmarks = []

    utils.drop_tables(config_macro.fmd_db)
    server_pid = utils.start_app(level, config_macro.webserver, config_macro.port,
                                 config_macro.url, 'macro.autoapp:app', log=False)
    time.sleep(config_macro.bm_cooldown)
    benchmark_file = configparser.ConfigParser()
    benchmark_file['bench'] = {'users': user}
    with open('bm_info.ini', 'w') as configfile:
        benchmark_file.write(configfile)

    with temporary_file() as tmp:
        cmd.extend(('--output', tmp))
        run_command(cmd)
        benchmarks.append(perf.Benchmark.load(tmp))

    utils.stop_app(server_pid)
    time.sleep(config_macro.bm_cooldown)

    return perf.BenchmarkSuite(benchmarks)


def test():
    server_pid = utils.start_app(-1, config_macro.webserver, config_macro.port,
                                 config_macro.url, 'macro.autoapp:app', log=True)
    print(server_pid)


def run():
    for user in config_macro.users:
        start_time = datetime.datetime.now().strftime("%y%m%d_%H:%M:%S")
        results_dir = LOCATION + '../results/macro/' + start_time
        set_environment('macro/autoapp.py')
        utils.create_results_dir(results_dir, MACRO_FILE)
        print("Concurrent users: %d" % user)
        for level in config_macro.levels:
            print("FMD level %d" % level)
            suite = run_perf_script(level, user)
            suite.dump(utils.get_file_name(results_dir, level))
