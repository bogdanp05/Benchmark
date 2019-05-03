import json
import random

from locust import HttpLocust, task, TaskSequence, seq_task
from locust.exception import StopLocust


class UserBehavior(TaskSequence):
    headers = {'content-type': 'application/json'}
    limit = 10
    offset = 0
    current_article = None

    def home(self):
        self.client.get("/api/articles/feed?limit=10&offset=0", headers=self.headers)
        self.client.get("/api/tags", headers=self.headers)

    def read_global_article(self):
        response = self.client.get("/api/articles?limit=%d&offset=%d" % (self.limit, self.offset),
                                   headers=self.headers)
        articles = [a['slug'] for a in response.json()['articles']]
        article = random.choice(articles)
        self.current_article = article
        self.client.get("/api/articles/%s" % article, headers=self.headers)
        self.client.get("/api/articles/%s/comments" % article, headers=self.headers)
        self.offset += self.limit

    def post_comment(self):
        payload = {"comment": {"body": "Nice article!"}}
        self.client.post("/api/articles/%s/comments" % self.current_article,
                         data=json.dumps(payload), headers=self.headers)

    def favorite_article(self):
        self.client.post("/api/articles/%s/favorite" % self.current_article, headers=self.headers)

    def write_article(self):
        uniques = random.sample(range(0, 1000), 3)
        payload = {"article": {"title": "title%d" % uniques[0],
                               "description": "description%d" % uniques[1],
                               "body": "%dA very short article." % uniques[2],
                               "tagList": ["tag1", "tag2"]}}
        response = self.client.post("/api/articles", data=json.dumps(payload), headers=self.headers)
        slug = response.json()['article']['slug']
        self.client.get("/api/articles/%s" % slug, headers=self.headers)
        self.client.get("/api/articles/%s/comments" % slug, headers=self.headers)

    @seq_task(1)
    def login(self):
        payload = {"user": {"email": "user1@user.com", "password": "user"}}
        response = self.client.post("/api/users/login", data=json.dumps(payload), headers=self.headers)
        self.headers['authorization'] = 'Token %s' % response.json()['user']['token']
        self.home()

    @seq_task(2)
    @task(3)
    def index_1(self):
        self.read_global_article()
        self.home()

    @seq_task(3)
    def comment_1(self):
        self.post_comment()

    @seq_task(4)
    @task(2)
    def index_2(self):
        self.read_global_article()
        self.home()

    @seq_task(5)
    def add_article(self):
        self.write_article()

    @seq_task(6)
    @task(2)
    def index_3(self):
        self.read_global_article()
        self.home()

    @seq_task(7)
    def fav(self):
        self.favorite_article()

    @seq_task(8)
    @task(3)
    def index_4(self):
        self.read_global_article()
        self.home()

    @seq_task(9)
    def stop(self):
        raise StopLocust


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 0
    max_wait = 0
