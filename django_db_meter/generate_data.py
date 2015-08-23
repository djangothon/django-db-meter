import random
import threading

from django.contrib.auth.models import User
from models import TestModel


def generate_queries():
    u1 = User.objects.filter()

    new_name = str(random.randint(0, 2000000))
    if u1:
        u1.update(first_name=new_name)
    else:
        u1 = User(username=new_name)
        u1.save()

    u1 = User.objects.filter(username=new_name)
    if u1:
	u1 = u1[0]
        u1.first_name = new_name + 'hello'
        u1.save()

    users = [User(username=get_random_text()) for i in xrange(100)]
    for user in users:
        user.save()
	u = User.objects.filter(username=user.username)
	if u.exists():
		username = u[0].username + 'dfas'
		u.update(username=username)
    t = TestModel.objects.filter(user=u1)
    t = list(t)

    for i in xrange(100):
        t = TestModel.objects.filter()
        t = list(t)

    for i in xrange(len(users)):
        random_user = random.choice(users)
        t = TestModel(user=random_user)
        t.save()

    for i in xrange(100):
        k = TestModel.objects.select_related('user')
        k = list(k)
    tm = TestModel.objects.all()
    for t in tm:
	t.delete()


def get_random_text():
    new_name = str(random.randint(0, 2000000))
    return new_name


def main(concurrency=2):
    ths = [threading.Thread(target=generate_queries) for i in
            xrange(concurrency)]
    for th in ths:
        th.start()

    for th in ths:
        th.join()
