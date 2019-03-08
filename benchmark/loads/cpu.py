from performance.benchmarks import bm_pidigits, bm_float


def pi_digits_bm():
    bm_pidigits.calc_ndigits(bm_pidigits.DEFAULT_DIGITS)


def float_bm():
    bm_float.benchmark(bm_float.POINTS)
