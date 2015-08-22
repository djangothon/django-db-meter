from base import BaseAsyncClient
from threading import Thread

class ThreadAsyncClient(BaseAsyncClient):

    def execute(self, callback, msg):
        t = Thread(callback, msg)
        t.start()

