import datetime
import os

from caller import utils, config_macro, LOCATION, MACRO_FILE

START_TIME = datetime.datetime.now().strftime("%y%m%d_%H:%M:%S")
RESULTS_DIR = LOCATION + '../results/macro/' + START_TIME


def set_environment(flask_app):
    os.environ["FLASK_APP"] = LOCATION + '../' + flask_app


def run():
    set_environment('macro/autoapp.py')
    utils.create_results_dir(RESULTS_DIR, MACRO_FILE)
    server_pid = utils.start_app(0, config_macro.webserver, config_macro.port, config_macro.url, 'macro.autoapp:app')
    print(server_pid)
