class BaseAsyncClient(object):
    """Base class for all the async executors that are supported.
    """

    def execute(self, callback, msg):
        """Common method for sending messages
        """

        raise NotImplementedError

