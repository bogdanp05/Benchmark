import os
import shutil
import signal
import subprocess
import sys

from sqlalchemy import create_engine, MetaData, exc

from caller import LOCATION

APP_OUTPUT = LOCATION + '../output.log'


def create_results_dir(results_dir, config_file):
    os.mkdir(results_dir)
    shutil.copy2(config_file, results_dir)


def set_environment(flask_app, fmd_db=None, bm_speed=None):
    os.environ["FLASK_APP"] = LOCATION + '../' + flask_app
    os.environ["FMD_DB"] = fmd_db
    os.environ["BM_SPEED"] = bm_speed


def drop_tables(db_url):
    try:
        engine = create_engine(db_url)
        meta = MetaData(bind=engine)
        meta.reflect()
        for tbl in reversed(meta.sorted_tables):
            engine.execute(tbl.delete())
    except exc.InternalError as e:
        print(e)
        sys.exit(1)


def start_app(fmd_level, webserver, port, url):
    os.environ["FMD_LEVEL"] = str(fmd_level)
    command = []
    if webserver == 'werkzeug':
        command.extend(["flask", "run", "-p", port])
    else:
        command.extend(["gunicorn", "-w", "1", "-b", url + ':' + port, "micro.app:app"])

    with open(APP_OUTPUT, 'a') as f:
        server_process = subprocess.Popen(command, stdout=f)
    return server_process.pid


def stop_app(server_pid):
    os.kill(server_pid, signal.SIGTERM)
