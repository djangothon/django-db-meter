class BaseMessageBroker(object):
    """Base message broker for all the supported message queues as well as
    databases.
    """

    def send(self, msg):

        raise NotImplementedError
