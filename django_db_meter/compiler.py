from datetime import datetime

from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.constants import MULTI

from django_db_meter.message import DBMetric

from models import (DBWiseAggregatedMetric, AppWiseAggregatedMetric,
                    TableWiseAggregatedMetric, DBQueryMetric)

EXCLUDE_MODELS = [DBWiseAggregatedMetric, AppWiseAggregatedMetric,
        TableWiseAggregatedMetric, DBQueryMetric]


class CustomSQLCompiler(SQLCompiler):
    """
    Custom SQL compiler which overrides the execute_sql method of django's
    SQLCompiler class to log the queries asynchronously in a database for
    builing realtime metrics over them.
    """

    def execute_sql(self, result_type=MULTI):
        query_start_time = datetime.now()
        result = super(CustomSQLCompiler, self).execute_sql(result_type)

        # do not report db_meter tables
        if self.query.model in EXCLUDE_MODELS:
            return result

        query_end_time = datetime.now()
        extra_kwargs = {
            'query_start_time': query_start_time,
            'query_execution_time': (query_end_time -
                query_start_time).total_seconds(),
            'rows_affected': len(list(result)),
            'db': self.using
        }
        metric = DBMetric.from_query(self.query, **extra_kwargs)
        metric.send()
        return result
        #metric.send()

