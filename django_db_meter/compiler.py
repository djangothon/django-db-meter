from datetime import datetime

from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.constants import MULTI

from django_db_meter.message import DBMetric

class CustomSQLCompiler(SQLCompiler):
    """
    Custom SQL compiler which overrides the execute_sql method of django's
    SQLCompiler class to log the queries asynchronously in a database for
    builing realtime metrics over them.
    """

    def execute_sql(self, result_type=MULTI):
        query_start_time = datetime.now()
        result = super(CustomSQLCompiler, self).execute_sql(result_type)
        query_end_time = datetime.now()
        result.query_start_time = query_start_time
        result.query_execution_time = query_end_time - query_start_time
        metric = DBMetric.from_queryset(result)
        metric.send()

