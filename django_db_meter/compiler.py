import six

from datetime import datetime

from django.db.models.sql.compiler import (SQLCompiler, SQLInsertCompiler,
        SQLUpdateCompiler, SQLAggregateCompiler, SQLDeleteCompiler)

from django.db.backends.mysql.compiler import (SQLCompiler as MySQLCompiler,
        SQLInsertCompiler as MySQLInsertCompiler, SQLDeleteCompiler as
        MySQLDeleteCompiler, SQLUpdateCompiler as MySQLUpdateCompiler,
        SQLAggregateCompiler as MySQLAggregateCompiler)

from django.db.models.sql.constants import MULTI

from django_db_meter.message import DBMetric

from models import (DBWiseAggregatedMetric, AppWiseAggregatedMetric,
                    TableWiseAggregatedMetric, DBQueryMetric)

EXCLUDE_MODELS = [DBWiseAggregatedMetric, AppWiseAggregatedMetric,
        TableWiseAggregatedMetric, DBQueryMetric]


class MetricCreator(object):

    _query_start_time = None
    _query_end_time = None

    def _create_metric_object(self, result):
        if result.__class__ == self.connection.cursor().__class__:
            return
        query_start_time = self._query_start_time
        if self.query.model in EXCLUDE_MODELS:
            return result

        query_end_time = self._query_end_time
        rows_affected = 0
        if type(result) == list:
            rows_affected = len(result)

        if isinstance(result, six.integer_types):
            if issubclass(self.__class__, CustomSQLInsertCompiler):
                rows_affected = 1
            if issubclass(self.__class__, CustomSQLUpdateCompiler):
                rows_affected = result
        query_execution_time = 0.0
        if (query_start_time is not None and query_end_time is not None):
            query_execution_time = query_end_time - query_start_time
            query_execution_time = query_execution_time.total_seconds()
        query_sql = self._get_query_sql(self.as_sql())
        extra_kwargs = {
            'query_start_time': query_start_time,
            'query_execution_time': query_execution_time,
            'rows_affected': rows_affected,
            'query_sql': query_sql,
            'query_type': self._get_query_type(query_sql),
            'db': self.using,
        }
        metric = DBMetric.from_query(self.query, **extra_kwargs)
        metric.send()

    @classmethod
    def _get_query_sql(cls, query_sql):
        query_sql = query_sql[0]
        if type(query_sql) == tuple:
            query_sql = query_sql[0]
        return query_sql


    @classmethod
    def _get_query_type(cls, query_sql):
        print "Query SQL ", query_sql, type(query_sql)
        if 'SELECT' in query_sql:
            return 'SELECT'
        if 'INSERT' in query_sql:
            return 'INSERT'

        if 'UPDATE' in query_sql:
            return 'UPDATE'
        if 'DELETE' in query_sql:
            return 'DELETE'

class CustomSQLCompiler(SQLCompiler, MetricCreator):
    """
    Custom SQL compiler which overrides the execute_sql method of django's
    SQLCompiler class to log the queries asynchronously in a database for
    builing realtime metrics over them.
    """

    def execute_sql(self, result_type=MULTI):
        self._query_start_time = datetime.now()
        result = super(CustomSQLCompiler, self).execute_sql(result_type)
        self._query_end_time = datetime.now()
        self._create_metric_object(result)
        return result

class CustomSQLInsertCompiler(SQLInsertCompiler, CustomSQLCompiler):
    def execute_sql(self, return_id=False):
        self._query_start_time = datetime.now()
        result = super(CustomSQLInsertCompiler,
                self).execute_sql(return_id=return_id)
        self._query_end_time = datetime.now()
        self._create_metric_object(result)
        return result

class CustomSQLUpdateCompiler(SQLUpdateCompiler, CustomSQLCompiler):
    def execute_sql(self, result_type):
        self._query_start_time = datetime.now()
        result = super(CustomSQLUpdateCompiler,
                self).execute_sql(result_type)
        self._query_end_time = datetime.now()
        self._create_metric_object(result)
        return result

class CustomSQLDeleteCompiler(SQLDeleteCompiler, CustomSQLCompiler):
    pass

class CustomSQLAggregateCompiler(SQLAggregateCompiler, CustomSQLCompiler):
    pass

class CustomMySQLCompiler(MySQLCompiler, CustomSQLCompiler):
    pass

class CustomMySQLInsertCompiler(CustomSQLInsertCompiler, CustomMySQLCompiler):
    pass

class CustomMySQLUpdateCompiler(CustomSQLUpdateCompiler, CustomMySQLCompiler):
    pass

class CustomMySQLDeleteCompiler(CustomSQLDeleteCompiler, CustomMySQLCompiler):
    pass

class CustomMySQLAggregateCompiler(CustomSQLAggregateCompiler, CustomMySQLCompiler):
    pass
