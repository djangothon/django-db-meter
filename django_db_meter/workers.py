from brokers.rabbitmq import RabbitMQConsumer
from message import DBMetric

from models import (DBQueryMetric, DBWiseAggregatedMetric,
                    TableWiseAggregatedMetric, AppWiseAggregatedMetric)


class DBMetricsConsumer(RabbitMQConsumer):
    def __init__(self, routing_key="django_db_meter"):
        super(DBMetricsConsumer, self).__init__(routing_key=routing_key)

    def on_message(self, message):
        message = DBMetric.deserialize(message)

        print message
        if not message:
            return

        db_metric = message
        kwargs = db_metric.as_dict()
        DBQueryMetric.create_object(**kwargs)
        DBWiseAggregatedMetric.aggregate_metric(db_metric)
        TableWiseAggregatedMetric.aggregate_metric(db_metric)
        AppWiseAggregatedMetric.aggregate_metric(db_metric)


def run_metrics_consumer():
    consumer = DBMetricsConsumer()
    consumer.consume()
