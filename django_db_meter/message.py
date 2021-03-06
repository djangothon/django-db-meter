import datetime
import cPickle as pickle
import pylzma
import json

from collections import namedtuple
from django.core.serializers import serialize, deserialize
from django.conf import settings

from brokers.rabbitmq import RabbitMQClient
from async.thread import ThreadAsyncClient


class DBMetric(object):
    def __init__(self, **kwargs):
        self.timestamp = kwargs.get('timestamp', datetime.datetime.now())
        self.query_start_time = kwargs.get('query_start_time')
        self.query_execution_time = kwargs.get('query_execution_time')
        self.query_sql = kwargs.get('query_sql')
        self.query_tables = kwargs.get('query_tables', [])
        self.query_type = kwargs.get('query_type')
        self.db_name = kwargs.get('db_name')
        self.app_name = kwargs.get('app_name')
        self.rows_affected = kwargs.get('rows_affected')

    def as_dict(self):
        data = {
            'timestamp': self.timestamp,
            'query_start_time': self.query_start_time,
            'query_execution_time': self.query_execution_time,
            'query_sql': self.query_sql,
            'query_tables': self.query_tables,
            'db_name': self.db_name,
            'app_name': self.app_name,
            'rows_affected': self.rows_affected,
            'query_type': self.query_type
        }
        return data

    def as_json(self):
        data = self.as_dict()
        data_json = json.dumps(data)
        return data_json

    @classmethod
    def from_query(cls, query, **kwargs):
        kwargs = {
            'timestamp': datetime.datetime.now(),
            'query_start_time': kwargs.get('query_start_time'),
            'query_execution_time': kwargs.get('query_execution_time'),
            'query_sql': kwargs.get('query_sql', ''),
            'query_tables': cls._get_query_tables(query),
            'db_name': cls._get_db_from_name(kwargs.get('db')),
            'app_name': query.model._meta.app_label,
            'rows_affected': kwargs.get('rows_affected', 0),
            'query_type': kwargs.get('query_type')
        }
        obj = cls(**kwargs)
        return obj

    @classmethod
    def _get_db_from_name(cls, name):
        return settings.DATABASES.get(name).get('NAME')

    @classmethod
    def _get_query_tables(self, query):
        return query.alias_map.keys()
        query_tables = query.tables
        if query.select_related:
            query_tables.extend(query.select_related.keys())
        return query_tables

    def serialize(self):
        serialized = pickle.dumps(self)
        compressed = pylzma.compress(serialized)
        return compressed

    @staticmethod
    def deserialize(message):
        decompressed_msg = pylzma.decompress(message)

        deserialized = pickle.loads(decompressed_msg)
        return deserialized

    def send(self):
        client = RabbitMQClient(routing_key="django_db_meter")
        serialized_message = self.serialize()
        async_client = ThreadAsyncClient()
        async_client.execute(client.send, serialized_message)
