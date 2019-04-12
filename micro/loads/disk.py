from micro.loads.ported_benchmarks import bm_sqlalchemy
from micro.loads import SQL_WRITES, SQL_READS, FILE_WRITES, FILE_READS, SQL_COMBINED
import os

TEXT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et " \
       "dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip " \
       "ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu " \
       "fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt " \
       "mollit anim id est laborum.\n"
FILE_NAME = 'io.txt'


def sql_combined_bm():
    bm_sqlalchemy.bench_sqlalchemy(loops=SQL_COMBINED, writes=2, reads=17)


def sql_writes():
    bm_sqlalchemy.bench_sqlalchemy(loops=SQL_WRITES, writes=5, reads=0)


def sql_reads():
    bm_sqlalchemy.bench_sqlalchemy(loops=SQL_READS, writes=0, reads=30)


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
