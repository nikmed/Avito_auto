from random import randint

from locust import HttpUser, TaskSet, between


def index(l):
    l.client.get("/")


def redirect(l):
    l.client.get('/' + str(randint(1, 5)))


class UserTasks(TaskSet):
    tasks = [redirect]


class WebsiteUser(HttpUser):
    tasks = [UserTasks]
    wait_time = between(1, 5)
