import datetime
import os
import time

import perf
from performance.run import run_command
from performance.utils import temporary_file

from caller import utils, config_macro, LOCATION, MACRO_FILE

START_TIME = datetime.datetime.now().strftime("%y%m%d_%H:%M:%S")
RESULTS_DIR = LOCATION + '../results/macro/' + START_TIME
APP_PATH = config_macro.protocol + '://' +\
           config_macro.url + ':' +\
           config_macro.port + '/api'


def set_environment(flask_app):
    os.environ["FLASK_APP"] = LOCATION + '../' + flask_app
    os.environ["APP_DB"] = config_macro.app_db
    os.environ["FMD_DB"] = config_macro.fmd_db


def run_perf_script(level):
    bm_path = LOCATION + 'macro_script.py'
    cmd = list(["python"])
    cmd.append('-u')
    cmd.append(bm_path)

    benchmarks = []

    utils.drop_tables(config_macro.fmd_db)
    time.sleep(config_macro.bm_cooldown)
    # benchmark_file = configparser.ConfigParser()
    # benchmark_file['bench'] = {'name': b[0], 'desc': b[1]}
    # with open('bm_info.ini', 'w') as configfile:
    #     benchmark_file.write(configfile)

    with temporary_file() as tmp:
        cmd.extend(('--output', tmp))
        run_command(cmd)
        benchmarks.append(perf.Benchmark.load(tmp))

    # utils.stop_app(server_pid)
    # time.sleep(config_micro.bm_cooldown)

    return perf.BenchmarkSuite(benchmarks)


def get_file_name(results_dir, monitor_level):
    filename = results_dir + '/' + str(monitor_level) + '.json'
    return filename


def run():
    start_time = datetime.datetime.now().strftime("%y%m%d_%H:%M:%S")
    results_dir = LOCATION + '../results/macro/' + start_time
    set_environment('macro/autoapp.py')
    utils.create_results_dir(RESULTS_DIR, MACRO_FILE)
    server_pid = utils.start_app(1, config_macro.webserver, config_macro.port,
                                 config_macro.url, 'macro.autoapp:app', log=False)
    print(server_pid)

    for level in config_macro.levels:
        print("FMD level %d" % level)
        suite = run_perf_script(level)
        suite.dump(get_file_name(results_dir, level))
