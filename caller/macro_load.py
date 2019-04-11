import json
import time

import requests

from caller import utils, config_macro
from caller.macro import set_environment, APP_PATH

HEADERS = {'content-type': 'application/json'}
USERS = 10
USER_PREFIX = 'user'
PASSWORD = 'user'
ARTICLES = 10  # articles per user
ARTICLE_SIZE = 100  # in KB

# 1 KB text
LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin gravida facilisis mauris id tincidunt. " \
              "Phasellus eget turpis magna. Fusce tempus ullamcorper felis in pretium. Fusce viverra velit non odio " \
              "malesuada, non porta tellus convallis. Proin vel libero vel metus bibendum viverra. Cras dignissim " \
              "libero magna, nec sagittis nunc iaculis id. Sed varius non eros lacinia varius. Phasellus non rhoncus " \
              "nibh. Nullam rutrum elit ac tincidunt volutpat.\n Phasellus vitae aliquet neque. Phasellus venenatis " \
              "dui non neque condimentum tempus. Fusce nibh mauris, semper eu arcu nec, tristique interdum lorem. " \
              "Nam ac auctor velit, laoreet cursus tortor. Morbi bibendum sem erat, at maximus erat gravida eu. " \
              "Praesent accumsan maximus leo quis tincidunt. Donec dolor eros, porttitor vitae enim id, " \
              "interdum malesuada enim. Curabitur vitae condimentum mi.\n Nulla ac varius dui. Aliquam eu diam " \
              "molestie, posuere ipsum non, ultrices nulla. Aenean euismod efficitur est, eu fermentum dolor luctus " \
              "id. Aenean molestie cursus diam sit nullam.\n"


class User(object):
    def __init__(self, index):
        self.username = USER_PREFIX + str(index)
        self.email = self.username + '@user.com'
        self.password = PASSWORD
        self.auth_headers = None

    def register(self):
        payload = {'user': {'username': self.username, 'email': self.email, 'password': self.password}}
        response = requests.post(APP_PATH + '/users/', data=json.dumps(payload), headers=HEADERS)
        self.auth_headers = {'authorization': 'Token %s' % response.json()['user']['token']}


def create_users():
    users = []
    for i in range(USERS):
        user = User(i)
        user.register()
        users.append(user)
    return users


def get_article():
    article = ""
    for _ in range(ARTICLE_SIZE):
        article += LOREM_IPSUM
    return article


def create_articles():
    article = get_article()
    print(article)
    for u in range(USERS):
        pass


def create_load():
    set_environment('macro/autoapp.py')
    utils.drop_tables(config_macro.db)
    print("Deleted tables")
    server_pid = utils.start_app(-1, config_macro.webserver, config_macro.port,
                                 config_macro.url, 'macro.autoapp:app', log=True)
    time.sleep(5)
    users = create_users()
    print(users)
    # create_articles()
    utils.stop_app(server_pid)
