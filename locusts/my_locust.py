import json
import random

from locust import HttpLocust, task, TaskSequence, seq_task
from locust.exception import StopLocust


class UserBehavior(TaskSequence):
    auth_headers = None

    def home(self):
        self.client.get("/api/articles/feed?limit=10&offset=0", headers=self.auth_headers)
        self.client.get("/api/tags", headers=self.auth_headers)

    def read_global_article(self):
        response = self.client.get("/api/articles?limit=10&offset=0", headers=self.auth_headers)
        articles = [a['slug'] for a in response.json()['articles']]
        article = random.choice(articles)
        self.client.get("/api/articles/%s" % article, headers=self.auth_headers)
        self.client.get("/api/articles/%s/comments" % article, headers=self.auth_headers)

    @seq_task(1)
    def login(self):
        payload = {"user": {"email": "user3@user.com", "password": "user"}}
        headers = {'content-type': 'application/json'}
        response = self.client.post("/api/users/login", data=json.dumps(payload), headers=headers)
        self.auth_headers = {'authorization': 'Token %s' % response.json()['user']['token']}
        self.home()

    @seq_task(2)
    @task(10)
    def index(self):
        self.read_global_article()
        self.home()

    @seq_task(3)
    def stop(self):
        raise StopLocust


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 0
    max_wait = 0
