from datetime import datetime

from django.db import models

# Create your models here.


class DBQueryMetric(models.Model):
    """
    Model for storing a single query related data
    """

    timestamp = models.DateTimeField()
    query_start_time = models.DateTimeField()
    query_execution_time = models.FloatField(default=0.0)
    query_sql = models.TextField()
    query_tables = models.TextField()
    db_name = models.CharField(max_length=255)
    app_name = models.CharField(max_length=255)
    rows_affected = models.PositiveIntegerField(default=0)

    @staticmethod
    def create_object(**kwargs):
        return DBQueryMetric.objects.create(**kwargs)

    def is_joined_query(self):
        return 'JOIN' in self.query_sql or 'join' in self.query_sql

class BaseAggregatedMetric(models.Model):
    """
    Base model for storing aggregated data.
    """

    timestamp = models.DateTimeField()
    num_queries = models.PositiveIntegerField(default=0)
    average_query_time = models.FloatField(default=0.0)
    num_joined_queries = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True

    @staticmethod
    def get_total_query_time(obj, db_metric):
        return (obj.num_queries * obj.average_query_time + db_metric.query_execution_time)

    @classmethod
    def _aggregate_metric(cls, obj, db_metric):
        obj.num_queries = obj.num_queries + 1
        obj.query_time = BaseAggregatedMetric.get_total_query_time(obj,
                db_metric)/obj.num_queries
        if db_metric.is_joined_query():
            obj.num_joined_queries = obj.num_joined_queries + 1
        obj.save()

    @classmethod
    def aggregate_metric(cls, db_metric):
        raise NotImplementedError

    @staticmethod
    def get_manipulated_timestamp():
        return datetime.now().replace(second=0, microsecond=0)

class TableWiseAggregatedMetric(BaseAggregatedMetric):
    table_name = models.CharField(max_length=255)

    @classmethod
    def aggregate_metric(cls, db_metric):
        kwargs = {
            'table_name': db_metric.table_name,
            'timestamp': BaseAggregatedMetric.get_manipulated_timestamp(),
        }
        obj = cls.objects.filter(**kwargs)
        if not obj.exists():
            obj = cls.objects.create(**kwargs)
        cls._aggregate_metric(obj, db_metric)

class DBWiseAggregatedMetric(BaseAggregatedMetric):
    db_name = models.CharField(max_length=255)

    @classmethod
    def aggregate_metric(cls, db_metric):
        kwargs = {
            'db_name': db_metric.db_name,
            'timestamp': BaseAggregatedMetric.get_manipulated_timestamp(),
        }
        obj = cls.objects.filter(**kwargs)
        if not obj.exists():
            obj = cls.objects.create(**kwargs)
        cls._aggregate_metric(obj, db_metric)

class AppWiseAggregatedMetric(BaseAggregatedMetric):
    app_name = models.CharField(max_length=255)

    @classmethod
    def aggregate_metric(cls, db_metric):
        kwargs = {
            'app_name': db_metric.app_name,
            'timestamp': BaseAggregatedMetric.get_manipulated_timestamp(),
        }
        obj = cls.objects.filter(**kwargs)
        if not obj.exists():
            obj = cls.objects.create(**kwargs)
        cls._aggregate_metric(obj, db_metric)
