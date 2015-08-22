import json

from django.http import HttpResponse

from django_db_meter.models import AppWiseAggregatedMetric
from django_db_meter.models import TableWiseAggregatedMetric
from django_db_meter.models import DBWiseAggregatedMetric

# Create your views here.


def get_app_wise_data(request, app_name):
    data = AppWiseAggregatedMetric.objects.filter(
            app_name=app_name).order_by('-timestamp')[:40]
    response = [{
        'timestamp': data_point.timestamp,
        'num_queries': data_point.num_queries,
        'num_joined_queries': data_point.num_joined_queries,
        'average_query_time': data_point.average_query_time,
    } for data_point in data]

    response = json.dumps(response)
    response = HttpResponse(response, content_type='application/json')
    return response

def get_table_wise_data(request, table_name):
    data = TableWiseAggregatedMetric.objects.filter(
            table_name=table_name).order_by('-timestamp')[:40]
    response = [{
        'timestamp': data_point.timestamp,
        'num_queries': data_point.num_queries,
        'num_joined_queries': data_point.num_joined_queries,
    } for data_point in data]

    response = json.dumps(response)
    response = HttpResponse(response, content_type='application/json')
    return response

def get_db_wise_data(request, db_name):
    data = DBWiseAggregatedMetric.objects.filter(
            app_name=db_name).order_by('-timestamp')[:40]
    response = [{
        'timestamp': data_point.timestamp,
        'num_queries': data_point.num_queries,
        'num_joined_queries': data_point.num_joined_queries,
    } for data_point in data]

    response = json.dumps(response)
    response = HttpResponse(response, content_type='application/json')
    return response

