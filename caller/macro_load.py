import json
import random
import time

import requests

from caller import utils, config_macro
from caller.macro import set_environment, APP_PATH

USER_NUMBER = 100
USER_PREFIX = 'user'
PASSWORD = 'user'
ARTICLE_USER = 10  # articles per user
ARTICLE_SIZE = 100  # in KB
TITLE = 'Title'
DESCRIPTION = 'A short description of the article'
TAG = 'tag'
TAG_ARTICLE = 3  # tags per article
COMMENT = 'I really liked your article'
COMMENT_USER = 30  # comments from every user
FOLLOW_USER = 3
FAVORITE_ARTICLE = 3
PRINT_INTERVAL = 10
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
        self.index = index
        self.username = USER_PREFIX + str(index)
        self.email = self.username + '@user.com'
        self.password = PASSWORD
        self.headers = {'content-type': 'application/json'}

    def register(self):
        payload = {'user': {'username': self.username, 'email': self.email, 'password': self.password}}
        response = requests.post(APP_PATH + '/users/', data=json.dumps(payload), headers=self.headers)
        self.headers['authorization'] = 'Token %s' % response.json()['user']['token']

    def create_article(self, title, description, article, tags):
        payload = {'article': {'title': title, 'description': description, 'body': article, 'tagList': tags}}
        requests.post(APP_PATH + '/articles/', data=json.dumps(payload), headers=self.headers)

    def create_comment(self, slug, comment):
        payload = {'comment': {'body': comment}}
        requests.post(APP_PATH + '/articles/%s/comments' % slug, data=json.dumps(payload), headers=self.headers)

    def follow_user(self, username):
        requests.post(APP_PATH + '/profiles/%s/follow' % username, headers=self.headers)

    def favorite_article(self, slug):
        requests.post(APP_PATH + '/articles/%s/favorite' % slug, headers=self.headers)


def create_users():
    users = []
    for i in range(USER_NUMBER):
        user = User(i)
        user.register()
        users.append(user)
        if i % PRINT_INTERVAL == 0 and i > 0:
            print('Created %d of %d users' % (i, USER_NUMBER))
    return users


def generate_article_text():
    article = ""
    for _ in range(ARTICLE_SIZE):
        article += LOREM_IPSUM
    return article


def get_tags():
    return [TAG + str(i) for i in range(USER_NUMBER * ARTICLE_USER)]


def create_articles(users):
    article = generate_article_text()
    tags = get_tags()
    for idx, u in enumerate(users):
        if idx % PRINT_INTERVAL == 0 and idx > 0:
            print('Created %d of %d articles' % (idx*ARTICLE_USER, USER_NUMBER*ARTICLE_USER))
        for i in range(ARTICLE_USER):
            selected_tags = random.sample(population=tags, k=TAG_ARTICLE)
            u.create_article(title=TITLE + '_%d_%d' % (u.index, i), description=DESCRIPTION,
                             article=article, tags=selected_tags)


def get_articles():
    response = requests.get(APP_PATH + '/articles/?limit=%d' % (USER_NUMBER*ARTICLE_USER),
                            headers={'content-type': 'application/json'})
    return [a['slug'] for a in response.json()['articles']]


def create_comments_favorites(users):
    slugs = get_articles()
    for idx, u in enumerate(users):
        if idx % PRINT_INTERVAL == 0 and idx > 0:
            print('Created %d of %d comments' % (idx * COMMENT_USER, USER_NUMBER * COMMENT_USER))
        commented_slugs = random.sample(population=slugs, k=COMMENT_USER)
        for ss in commented_slugs:
            u.create_comment(ss, COMMENT)
        favorite_slugs = random.sample(population=slugs, k=FAVORITE_ARTICLE)
        for fs in favorite_slugs:
            u.favorite_article(fs)


def follow_favorite(users):
    usernames = [u.username for u in users]
    for idx, u in enumerate(users):
        if idx % PRINT_INTERVAL == 0 and idx > 0:
            print('Followed %d of %d users' % (idx * FOLLOW_USER, USER_NUMBER * FOLLOW_USER))
        others = set(usernames) - set(u.username)
        selected_users = random.sample(population=others, k=FOLLOW_USER)
        for su in selected_users:
            u.follow_user(su)


def create_load():
    set_environment('macro/autoapp.py')
    utils.drop_tables(config_macro.db)
    print("Deleted tables")
    server_pid = utils.start_app(-1, config_macro.webserver, config_macro.port,
                                 config_macro.url, 'macro.autoapp:app', log=False)
    time.sleep(5)
    users = create_users()
    print('Created %d users' % USER_NUMBER)
    create_articles(users)
    print('Created %d articles' % (USER_NUMBER * ARTICLE_USER))
    create_comments_favorites(users)
    print('Created %d comments' % (USER_NUMBER * COMMENT_USER))
    print('Favorite %d articles' % (USER_NUMBER * FAVORITE_ARTICLE))
    follow_favorite(users)
    print('Followed %d users' % (USER_NUMBER * FOLLOW_USER))

    utils.stop_app(server_pid)
