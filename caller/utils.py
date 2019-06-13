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


def start_app(fmd_level, webserver, port, url, app=None, log=False, output=None):
    os.environ["FMD_LEVEL"] = str(fmd_level)
    command = []
    if webserver == 'werkzeug':
        command.extend(["flask", "run", "-p", port])
    else:
        if not app:
            print("No app file given")
            return
        command.extend(["gunicorn", "-w", "4", "-b", url + ':' + port, app])
        if log:
            command.extend(["--log-level", "debug"])

    if output and output == 'console':
        server_process = subprocess.Popen(command)
    else:
        with open(APP_OUTPUT, 'a') as f:
            server_process = subprocess.Popen(command, stdout=f)

    return server_process.pid


def stop_app(server_pid):
    os.kill(server_pid, signal.SIGINT)


def get_file_name(results_dir, monitor_level):
    filename = results_dir + '/' + str(monitor_level) + '.json'
    return filename


def build_command(script):
    bm_path = LOCATION + script
    cmd = list(["python"])
    cmd.append('-u')
    cmd.append(bm_path)
    return cmd
