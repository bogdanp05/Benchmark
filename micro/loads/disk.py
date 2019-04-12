from micro.loads.ported_benchmarks import bm_sqlalchemy
from micro.loads import SQL_LOOPS, SQL_WRITES, SQL_READS, FILE_WRITES, FILE_READS
import os

TEXT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et " \
       "dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip " \
       "ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu " \
       "fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt " \
       "mollit anim id est laborum.\n"
FILE_NAME = 'io.txt'


def sql_combined_bm():
    bm_sqlalchemy.bench_sqlalchemy(loops=SQL_LOOPS, writes=SQL_WRITES, reads=SQL_READS)


def sql_writes():
    bm_sqlalchemy.bench_sqlalchemy(loops=SQL_LOOPS * 2, writes=SQL_WRITES, reads=0)


def sql_reads():
    bm_sqlalchemy.bench_sqlalchemy(loops=SQL_LOOPS, writes=0, reads=SQL_READS * 2)


def write_file():
    for _ in range(FILE_WRITES):
        try:
            os.remove(FILE_NAME)
        except FileNotFoundError:
            pass
        with open(FILE_NAME, 'w') as f:
            f.write(TEXT)


def read_file():
    try:
        for _ in range(FILE_READS):
            with open(FILE_NAME, 'r') as f:
                f.read()
    except FileNotFoundError:
        print("File %s does not exist. Benchmark aborted" % FILE_NAME)
