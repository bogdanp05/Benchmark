import configparser
import datetime
import time

import perf
from performance.run import run_command
from performance.utils import temporary_file

from caller import commons, config_micro, LOCATION, MICRO_FILE


START_TIME = datetime.datetime.now().strftime("%y%m%d_%H:%M:%S")
RESULTS_DIR = LOCATION + '../results/micro/' + START_TIME


def run_perf_script(level):
    bm_path = LOCATION + 'micro_script.py'
    cmd = list(["python"])
    cmd.append('-u')
    cmd.append(bm_path)

    benchmarks = []
    for b in config_micro.benchmarks:
        commons.drop_tables(config_micro.db_url)
        server_pid = commons.start_app(level, config_micro.webserver, config_micro.port, config_micro.url)
        time.sleep(config_micro.bm_cooldown)
        benchmark_file = configparser.ConfigParser()
        benchmark_file['bench'] = {'name': b[0], 'desc': b[1]}
        with open('bm_info.ini', 'w') as configfile:
            benchmark_file.write(configfile)

        with temporary_file() as tmp:
            cmd.extend(('--output', tmp))
            run_command(cmd)
            benchmarks.append(perf.Benchmark.load(tmp))

        commons.stop_app(server_pid)
        time.sleep(config_micro.bm_cooldown)

    return perf.BenchmarkSuite(benchmarks)


def get_file_name(monitor_level):
    filename = RESULTS_DIR + '/' + str(monitor_level) + '.json'
    return filename


def run():
    commons.set_environment('micro/app.py', config_micro.db_url, config_micro.speed)
    commons.create_results_dir(RESULTS_DIR, MICRO_FILE)
    for level in config_micro.levels:
        print("FMD level %d" % level)
        suite = run_perf_script(level)
        suite.dump(get_file_name(level))
