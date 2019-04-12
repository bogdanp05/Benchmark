import json
import shutil

from performance.benchmarks import bm_json_loads
from micro.loads.ported_benchmarks import bm_pathlib, bm_sqlalchemy
from micro.loads import JSON_LOOPS, POWERSET, PATH_LIB_NUM_FILES, PATH_LIB_LOOPS, MEMSQL_LOOPS


def json_loads_bm():
    json_dict = json.dumps(bm_json_loads.DICT)
    json_tuple = json.dumps(bm_json_loads.TUPLE)
    json_dict_group = json.dumps(bm_json_loads.DICT_GROUP)
    objs = (json_dict, json_tuple, json_dict_group)
    for _ in range(JSON_LOOPS):
        bm_json_loads.bench_json_loads(objs)


def powerset_bm():
    lst = list(range(0, POWERSET))
    result = [[]]
    for x in lst:
        result.extend([subset + [x] for subset in result])
    return result


def sqlmem_bm():
    bm_sqlalchemy.bench_sqlalchemy2(loops=MEMSQL_LOOPS)


def path_lib_bm():
    tmp_path = bm_pathlib.setup(PATH_LIB_NUM_FILES)
    try:
        bm_pathlib.bench_pathlib(loops=PATH_LIB_LOOPS, tmp_path=tmp_path, num_files=PATH_LIB_NUM_FILES)
    finally:
        shutil.rmtree(tmp_path)
