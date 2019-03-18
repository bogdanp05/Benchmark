import datetime
import logging
import timeit
from functools import wraps

from flask import Flask, jsonify

from benchmark import probe, FMD_LEVEL, LOCATION
from benchmark.loads import cpu, memory, disk

app = Flask(__name__)

if FMD_LEVEL > -1:
    print("FMD level: %d" % FMD_LEVEL)
    import flask_monitoringdashboard as dashboard
    # TODO: make this configurable
    db_url = 'sqlite:///' + LOCATION + '../fmd' + str(FMD_LEVEL) + '.db'
    dashboard.config.database_name = db_url
    dashboard.config.monitor_level = FMD_LEVEL
    dashboard.bind(app)


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/')
def root():
    return 'Server is running'


@app.route('/start_probe/<float:sampling_rate>')
def start_probe(sampling_rate):
    probe.start_probe(sampling_rate)
    return 'OK'


@app.route('/stop_probe/')
def stop_probe():
    probe.stop_probe()
    return 'OK'


def duration(func):
    @wraps(func)
    def decorated_function():
        t_0 = timeit.default_timer()
        func()
        t_1 = timeit.default_timer()
        response_time = t_1 - t_0
        print("%s: %s took %f seconds" % (datetime.datetime.now(), func.__name__, response_time))
        return jsonify({'response_time': response_time})
    return decorated_function


@app.route('/pidigits/')
@duration
def pi_digits_endpoint():
    cpu.pi_digits_bm()


@app.route('/float/')
@duration
def float_endpoint():
    cpu.float_bm()


@app.route('/json_loads/')
@duration
def json_loads_endpoint():
    memory.json_loads_bm()


@app.route('/path_lib/')
@duration
def path_lib_endpoint():
    memory.path_lib_bm()


@app.route('/sql_combined/')
@duration
def sql_combined_endpoint():
    disk.sql_combined_bm()


@app.route('/sql_writes/')
@duration
def sql_writes_endpoint():
    disk.sql_writes()


@app.route('/sql_reads/')
@duration
def sql_reads_endpoint():
    disk.sql_reads()


@app.route('/file_writes/')
@duration
def file_writes_endpoint():
    disk.write_file()


@app.route('/file_reads/')
@duration
def file_reads_endpoint():
    disk.read_file()
