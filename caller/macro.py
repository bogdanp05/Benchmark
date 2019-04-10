import datetime
import json
import os
import requests
import time

from caller import utils, config_macro, LOCATION, MACRO_FILE

START_TIME = datetime.datetime.now().strftime("%y%m%d_%H:%M:%S")
RESULTS_DIR = LOCATION + '../results/macro/' + START_TIME
APP_PATH = config_macro.protocol + '://' +\
           config_macro.url + ':' +\
           config_macro.port + '/api'


def set_environment(flask_app):
    os.environ["FLASK_APP"] = LOCATION + '../' + flask_app
    os.environ["MACRO_DB"] = config_macro.db


def run():
    set_environment('macro/autoapp.py')
    utils.create_results_dir(RESULTS_DIR, MACRO_FILE)
    server_pid = utils.start_app(-1, config_macro.webserver, config_macro.port, config_macro.url, 'macro.autoapp:app')
    print(server_pid)


def create_users(n):
    headers = {'content-type': 'application/json'}
    for i in range(n):
        username = 'user' + str(i)
        payload = {'user': {'username': 'user' + str(i),
                            'email': username + '@user.com',
                            'password': 'user'}}
        requests.post(APP_PATH + '/users', data=json.dumps(payload), headers=headers)


def create_load():
    set_environment('macro/autoapp.py')
    utils.drop_tables(config_macro.db)
    server_pid = utils.start_app(-1, config_macro.webserver, config_macro.port,
                                 config_macro.url, 'macro.autoapp:app', log=True)
    print("Deleted tables")
    time.sleep(5)
    create_users(10)
    utils.stop_app(server_pid)
