import datetime
import timeit

from flask import Flask, jsonify, request

from benchmark import probe, FMD_LEVEL, LOCATION
from benchmark.loads import cpu
from benchmark.loads import memory

app = Flask(__name__)

if FMD_LEVEL > -1:
    print("FMD level: %d" % FMD_LEVEL)
    import flask_monitoringdashboard as dashboard
    # TODO: make this configurable
    dashboard.config.database_name = 'sqlite:///' + LOCATION + '../fmd' + str(FMD_LEVEL) + '.db'
    dashboard.config.monitor_level = FMD_LEVEL
    dashboard.bind(app)


@app.route('/')
def root():
    return 'Server is running'


@app.route('/powerset/<int:n>')
def powerset(n):
    t0 = timeit.default_timer()
    memory.powerset(n)
    t_now = timeit.default_timer()
    response_time = t_now - t0
    print("%s: Finding power set of %d elements took %f seconds" %
          (datetime.datetime.utcnow(), n, response_time))
    response = {'response_time': response_time}
    return jsonify(response)


@app.route('/start_probe/<float:sampling_rate>')
def start_probe(sampling_rate):
    probe.start_probe(sampling_rate)
    return 'OK'


@app.route('/stop_probe/')
def stop_probe():
    probe.stop_probe()
    return 'OK'


@app.route('/pidigits/')
def pi_digits_endpoint():
    t0 = timeit.default_timer()
    cpu.pi_digits_bm()
    t_now = timeit.default_timer()
    response_time = t_now - t0
    print("%s: Finding 2000 digits of pi took %f seconds" %
          (datetime.datetime.now(), response_time))
    response = {'response_time': response_time}
    return jsonify(response)


@app.route('/float/')
def float_endpoint():
    t0 = timeit.default_timer()
    cpu.float_bm()
    t_now = timeit.default_timer()
    response_time = t_now - t0
    print("%s: Creating 100k point objects took %f seconds" %
          (datetime.datetime.now(), response_time))
    response = {'response_time': response_time}
    return jsonify(response)


@app.route('/json_loads/')
def json_loads_endpoint():
    t0 = timeit.default_timer()
    memory.json_loads_bm()
    t_now = timeit.default_timer()
    response_time = t_now - t0
    print("%s: Loading json objects took %f seconds" %
          (datetime.datetime.now(), response_time))
    response = {'response_time': response_time}
    return jsonify(response)


@app.route('/path_lib/')
def path_lib_endpoint():
    t0 = timeit.default_timer()
    memory.path_lib_bm()
    t_now = timeit.default_timer()
    response_time = t_now - t0
    print("%s: Pathlib operations took %f seconds" %
          (datetime.datetime.now(), response_time))
    response = {'response_time': response_time}
    return jsonify(response)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
