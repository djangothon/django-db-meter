from base import BaseAsyncClient
from threading import Thread

class ThreadAsyncClient(BaseAsyncClient):

    def execute(self, callback, msg):
        t = Thread(target=callback, args=(msg,))
        t.start()

