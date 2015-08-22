import json
import pika

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from base import BaseMessageBroker

class BaseRabbitMQ(BaseMessageBroker):
    def _connect(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RABBITMQ_ENDPOINT))
        self.connection = connection

    def __init__(self, routing_key, exchange=''):
        self.routing_key = routing_key
        self.exchange = exchange
        self._connect()
        channel = self.connection.channel()
        channel.queue_declare(queue=routing_key)
        self.channel = channel


class RabbitMQClient(BaseRabbitMQ):
    def send(self, msg):
        msg_json = json.dumps(msg, cls=DjangoJSONEncoder)
        publish_kwargs = {
            'exchange': self.exchange,
            'routing_key': self.routing_key,
            'body': msg_json
        }
        self.channel.basic_publish(**publish_kwargs)
        self.connection.close()

class RabbitMQConsumer(BaseRabbitMQ):
    def _on_message(self, ch, method, properties, body):
        self.on_message(body)

    def on_message(self, msg):
        print msg
        #raise NotImplementedError

    def consume(self):
        consume_kwargs = {
            'queue': self.routing_key,
            'no_ack': True,
        }
        self.channel.basic_consume(self._on_message, **consume_kwargs)
        self.channel.start_consuming()
