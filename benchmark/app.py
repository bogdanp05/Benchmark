import timeit

from flask import Flask

from benchmark import cpu, memory

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


@app.route('/factorial/<int:n>')
def factorial(n):
    t0 = timeit.default_timer()
    cpu.factorial(n)
    t_now = timeit.default_timer()
    print("Calculating factorial of %d took %f seconds" % (n, t_now - t0))
    return 'OK'


@app.route('/primes/<int:n>')
def primes(n):
    t0 = timeit.default_timer()
    cpu.find_primes(n)
    t_now = timeit.default_timer()
    print("Finding primes less than %d took %f seconds" % (n, t_now - t0))
    return 'OK'


@app.route('/powerset/<int:n>')
def powerset(n):
    t0 = timeit.default_timer()
    memory.powerset(n)
    t_now = timeit.default_timer()
    print("Finding power set of %d elements took %f seconds" % (n, t_now - t0))
    return 'OK'

