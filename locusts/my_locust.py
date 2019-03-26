import json
import random

from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):
    auth_headers = None

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def login(self):
        payload = {"user": {"email": "admin@admin.com", "password": "admin"}}
        headers = {'content-type': 'application/json'}
        response = self.client.post("/api/users/login", data=json.dumps(payload), headers=headers)
        self.auth_headers = {'authorization': 'Token %s' % response.json()['user']['token']}
        self.home()

    def home(self):
        self.client.get("/api/articles/feed?limit=10&offset=0", headers=self.auth_headers)
        self.client.get("/api/tags", headers=self.auth_headers)

    @task(2)
    def read_global_article(self):
        response = self.client.get("/api/articles?limit=10&offset=0", headers=self.auth_headers)
        articles = [a['slug'] for a in response.json()['articles']]
        article = random.choice(articles)
        self.client.get("/api/articles/%s" % article, headers=self.auth_headers)
        self.client.get("/api/articles/%s/comments" % article, headers=self.auth_headers)

    @task(1)
    def index(self):
        self.home()


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 5000
