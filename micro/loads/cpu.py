from performance.benchmarks import bm_pidigits, bm_float
from micro import config

DIGITS = 1300 if config.speed == "fast" else 2000
POINTS = 45000 if config.speed == "fast" else 100000


def pi_digits_bm():
    bm_pidigits.calc_ndigits(DIGITS)


def float_bm():
    bm_float.benchmark(POINTS)
