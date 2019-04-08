from performance.benchmarks import bm_pidigits, bm_float
from micro.loads import PI_DIGITS, FLOAT_POINTS


def pi_digits_bm():
    bm_pidigits.calc_ndigits(PI_DIGITS)


def float_bm():
    bm_float.benchmark(FLOAT_POINTS)
