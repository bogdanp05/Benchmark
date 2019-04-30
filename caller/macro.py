import datetime
import os

from caller import utils, config_macro, LOCATION, MACRO_FILE

START_TIME = datetime.datetime.now().strftime("%y%m%d_%H:%M:%S")
RESULTS_DIR = LOCATION + '../results/macro/' + START_TIME
APP_PATH = config_macro.protocol + '://' +\
           config_macro.url + ':' +\
           config_macro.port + '/api'


def set_environment(flask_app):
    os.environ["FLASK_APP"] = LOCATION + '../' + flask_app
    os.environ["APP_DB"] = config_macro.app_db
    os.environ["FMD_DB"] = config_macro.fmd_db


def run():
    set_environment('macro/autoapp.py')
    utils.create_results_dir(RESULTS_DIR, MACRO_FILE)
    server_pid = utils.start_app(-1, config_macro.webserver, config_macro.port, config_macro.url, 'macro.autoapp:app')
    print(server_pid)




