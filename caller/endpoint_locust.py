from locust import HttpLocust, task, TaskSequence, seq_task
from locust.exception import StopLocust


class UserBehavior(TaskSequence):
    headers = {'content-type': 'application/json'}

    def call_endpoint(self):
        while True:
            response = self.client.get("/sql_combined/", headers=self.headers)
            if response.ok:
                break

    @seq_task(1)
    @task(12500)
    def endpoint(self):
        self.call_endpoint()

    @seq_task(2)
    def stop(self):
        raise StopLocust


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 0
    max_wait = 0
