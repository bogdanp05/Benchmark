import json
import shutil

from performance.benchmarks import bm_json_loads
from benchmark.loads.ported_benchmarks import bm_pathlib

PATH_LIB_LOOPS = 6
PATH_LIB_NUM_FILES = 400
JSON_LOOPS = 200


def json_loads_bm():
    json_dict = json.dumps(bm_json_loads.DICT)
    json_tuple = json.dumps(bm_json_loads.TUPLE)
    json_dict_group = json.dumps(bm_json_loads.DICT_GROUP)
    objs = (json_dict, json_tuple, json_dict_group)
    for _ in range(JSON_LOOPS):
        bm_json_loads.bench_json_loads(objs)


def path_lib_bm():
    tmp_path = bm_pathlib.setup(PATH_LIB_NUM_FILES)
    try:
        bm_pathlib.bench_pathlib(loops=PATH_LIB_LOOPS, tmp_path=tmp_path, num_files=PATH_LIB_NUM_FILES)
    finally:
        shutil.rmtree(tmp_path)
