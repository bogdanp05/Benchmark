from performance.benchmarks import bm_pidigits, bm_float, bm_nbody
from micro.loads import PI_DIGITS, FLOAT_POINTS, NBODY_ITER


def pi_digits_bm():
    bm_pidigits.calc_ndigits(PI_DIGITS)


def float_bm():
    bm_float.benchmark(FLOAT_POINTS)


def nbody_bm():
    bm_nbody.bench_nbody(loops=1, reference=bm_nbody.DEFAULT_REFERENCE, iterations=NBODY_ITER)
