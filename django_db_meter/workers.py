from brokers.rabbitmq import RabbitMQConsumer
from message import DBMetric

from models import (DBQueryMetric, DBWiseAggregatedMetric,
                    TableWiseAggregatedMetric, AppWiseAggregatedMetric)


class DBMetricsConsumer(RabbitMQConsumer):
    def __init__(self, routing_key="django_db_meter"):

    
    def on_message(self, message):
        message = DBMetric.deserialize(message)

        if not message:
            return

        db_metric = message
        kwargs = db_metric.as_dict()
        DBQueryMetric.create_object(**kwargs)
        DBWiseAggregatedMetric.aggregate_metric(db_metric)
        TableWiseAggregatedMetric.aggregate_metric(db_metric)
        AppWiseAggregatedMetric.aggregate_metric(db_metric)
