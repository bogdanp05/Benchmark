from benchmark.loads.ported_benchmarks import bm_sqlalchemy

ROWS = 10
LOOPS = 5


def sql_declarative_bm():
    bm_sqlalchemy.bench_sqlalchemy_declarative(loops=LOOPS, npeople=ROWS)


def sql_imperative_bm():
    bm_sqlalchemy.bench_sqlalchemy_imperative(loops=LOOPS, npeople=ROWS)
