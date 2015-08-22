import datetime
import cPickle as pickle
import pylzma
import json

from collections import namedtuple
from django.core.serializers import serialize, deserialize
from django.conf import settings
from core.log import sclient
from core.utils import run_async

from newsfeed.activity import Actor, Target
from newsfeed.constants import NEWSFEED_QUEUE_NAME
from newsfeed.config import FeedConfig

from realtime.kafka.producer import KafkaProducer


class DBMetric(object):
    def __init__(**kwargs):
        self.timestamp = kwargs.get('timestamp', datetime.datetime.now())
        self.query_start_time = kwargs.get('query_start_time')
        self.query_execution_time = kwargs.get('query_execution_time')
        self.query_sql = kwargs.get('query_sql')
        self.query_tables = kwargs.get('query_tables', [])
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
            'rows_affected': self.rows_affected
        }
        return data

    def as_json(self):
        data = self.as_dict()
        data_json = json.dumps(data)
        return data_json

    @classmethod
    def from_queryset(cls, queryset):
        kwargs = {
            'timestamp': datetime.datetime.now(),
            'query_start_time': queryset.query_start_time,
            'query_execution_time': queryset.query_execution_time,
            'query_sql': queryset.query.__str__(),
            'query_tables': self._get_query_tables(queryset),
            'db_name': self._get_db_name(queryset),
            'app_name': queryset.model._meta.app_label,
            'rows_affected': queryset.count(),
        }
        obj = cls(**kwargs)
        return obj

    def send(self):
        msg_json = self.as_json()


    @classmethod
    def _get_db(cls, queryset):
        return settings.DATABASES.get(queryset.db).get('NAME')

    @classmethod
    def _get_query_tables(self, queryset):
        query_tables = queryset.tables
        query_tables.extend(queryset.select_related.keys())
        return query_tables

    def serialize(self):
        #self.obj = serialize('json', [self.obj])
        #print self.obj
        serialized = pickle.dumps(self)
        compressed = pylzma.compress(serialized)
        return compressed

    @staticmethod
    def deserialize(compressed_feed_message):
        decompressed_msg = pylzma.decompress(compressed_feed_message)

        deserialized = pickle.loads(decompressed_msg)
        return deserialized

    @classmethod
    def send_metric(cls, actor_ctype, actor_object_id, action, target_ctype,
            target_object_id, properties={},
            activity_datetime=None,
            activity_source=None):

        msg = cls(actor_ctype=actor_ctype,
                  actor_object_id=actor_object_id,
                  action=action,
                  target_ctype=target_ctype,
                  target_object_id=target_object_id,
                  properties=properties,
                  activity_datetime=activity_datetime,
                  activity_source=activity_source)
        msg.send()


    def send(self):
