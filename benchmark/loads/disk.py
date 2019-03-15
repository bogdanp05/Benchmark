from benchmark.loads.ported_benchmarks import bm_sqlalchemy
from benchmark import config

# TODO: make this configurable
LOOPS = 2 if config.speed == 'fast' else 3
WRITES = 5 if config.speed == 'fast' else 7
READS = 50 if config.speed == 'fast' else 70


def sql_combined_bm():
    bm_sqlalchemy.bench_sqlalchemy_combined(loops=LOOPS, writes=WRITES, reads=READS)


def sql_writes():
    bm_sqlalchemy.bench_sqlalchemy_combined(loops=LOOPS*2, writes=WRITES, reads=0)


def sql_reads():
    bm_sqlalchemy.bench_sqlalchemy_combined(loops=LOOPS, writes=0, reads=READS*2)
