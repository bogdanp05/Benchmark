import json

from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):
    article_name = "article2"
    token = None

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def login(self):
        payload = {"user": {"email": "admin@admin.com", "password": "admin"}}
        headers = {'content-type': 'application/json'}
        response = self.client.post("/api/users/login", data=json.dumps(payload), headers=headers)
        self.token = response.json()['user']['token']
        # self.client.get("/api/tags")

        auth_headers = {'authorization': 'Token %s' % self.token}
        self.client.get("/api/articles/feed?limit=10&offset=0", headers=auth_headers)

    @task(1)
    def task(self):
        self.client.get("/api/tags")

    # @task(1)
    # def global_articles(self):
    #     self.client.get("/api/articles?limit=10&offset=0")
    #
    # @task(1)
    # def article(self):
    #     self.client.get("/api/articles/%s" % self.article_name)
    #     self.client.get("/api/articles/%s/comments" % self.article_name)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 2000
    max_wait = 3000
