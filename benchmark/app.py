import timeit

from flask import Flask

from benchmark import cpu

app = Flask(__name__)


@app.route('/endpoint')
def endpoint3():
    return 'Ok'


@app.route('/pi/<int:precision>')
def pi(precision):
    t0 = timeit.default_timer()
    cpu.pi(precision)
    t_now = timeit.default_timer()
    print("Calculating pi with %d digits precision took %f seconds" % (precision, t_now - t0))
    return 'OK'
