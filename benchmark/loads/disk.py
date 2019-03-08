from benchmark.loads.ported_benchmarks import bm_sqlalchemy

# TODO: make this configurable
LOOPS = 3
WRITES = 7
READS = 70


def sql_combined_bm():
    bm_sqlalchemy.bench_sqlalchemy_combined(loops=LOOPS, writes=WRITES, reads=READS)


def sql_writes():
    bm_sqlalchemy.bench_sqlalchemy_combined(loops=LOOPS*2, writes=WRITES, reads=0)


def sql_reads():
    bm_sqlalchemy.bench_sqlalchemy_combined(loops=LOOPS, writes=0, reads=READS*2)
