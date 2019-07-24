import logging
import timeit
from functools import wraps

from flask import Flask, jsonify

from micro import FMD_LEVEL, FMD_DB
from micro.loads import cpu, memory, disk, recursive

app = Flask(__name__)

if FMD_LEVEL > -1:
    print("FMD level: %d" % FMD_LEVEL)
    import flask_monitoringdashboard as dashboard
    if FMD_DB:
        dashboard.config.database_name = FMD_DB
    dashboard.config.monitor_level = FMD_LEVEL
    dashboard.config.sampling_period = 5/1000.0
    dashboard.bind(app)


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/')
def root():
    return 'Server is running'


def duration(func):
    @wraps(func)
    def decorated_function():
        t_0 = timeit.default_timer()
        func()
        t_1 = timeit.default_timer()
        response_time = t_1 - t_0
        # print("%s: %s took %f seconds" % (datetime.datetime.now(), func.__name__, response_time))
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


@app.route('/nbody/')
@duration
def nbody_endpoint():
    cpu.nbody_bm()


@app.route('/fib/')
@duration
def fib_endpoint():
    recursive.fibonacci_bm()


@app.route('/json_loads/')
@duration
def json_loads_endpoint():
    memory.json_loads_bm()


@app.route('/list/')
@duration
def list_endpoint():
    memory.lists_bm()


@app.route('/powerset/')
@duration
def powerset_endpoint():
    memory.powerset_bm()


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


@app.route('/zero/')
def zero_endpoint():
    return 'OK'


@app.route('/file_writes/')
@duration
def file_writes_endpoint():
    disk.write_file()


@app.route('/file_reads/')
@duration
def file_reads_endpoint():
    disk.read_file()
