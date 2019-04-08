"""
Test the performance of pathlib operations.

This micro stresses the creation of small objects, globbing, and system
calls.
"""

import os
import pathlib
import tempfile


def generate_filenames(tmp_path, num_files):
    i = 0
    while num_files:
        for ext in [".py", ".txt", ".tar.gz", ""]:
            i += 1
            yield os.path.join(tmp_path, str(i) + ext)
            num_files -= 1


def setup(num_files):
    tmp_path = tempfile.mkdtemp()
    for fn in generate_filenames(tmp_path, num_files):
        with open(fn, "wb") as f:
            f.write(b'micro')

    return tmp_path


def bench_pathlib(loops, tmp_path, num_files):
    base_path = pathlib.Path(tmp_path)

    # Warm up the filesystem cache and keep some objects in memory.
    path_objects = list(base_path.iterdir())
    for p in path_objects:
        p.stat()
    assert len(path_objects) == num_files, len(path_objects)

    range_it = range(loops)

    for _ in range_it:
        # Do something simple with each path.
        for p in base_path.iterdir():
            p.stat()
        for p in base_path.glob("*.py"):
            p.stat()
        for p in base_path.iterdir():
            p.stat()
        for p in base_path.glob("*.py"):
            p.stat()
