import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.db.models import get_apps, get_models
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder

from django_db_meter.models import AppWiseAggregatedMetric
from django_db_meter.models import TableWiseAggregatedMetric
from django_db_meter.models import DBWiseAggregatedMetric

# Create your views here.

def index(request):
    ctx = {}
    template = 'index.html'
    return render(request, template, ctx)

def list_apps(request, app_name=None):
    template = 'index.html'
    if app_name is None:
        ctx = {
            'apps': [app.__package__.split('.')[-1] for app in get_apps()]
        }
    else:
        ctx = {'url': reverse('app_wise_data', args=(app_name,))}
    return render(request, template, ctx)

def list_tables(request, table_name=None):
    template = 'index.html'
    if table_name is None:
        tables = []
        for app in get_apps():
            for model in get_models(app):
                tables.append(model._meta.db_table)
        ctx = {
            'tables': tables
        }
    else:
        ctx = {'url': reverse('table_wise_data', args=(table_name,))}
    return render(request, template, ctx)

def list_dbs(request, db_name=None):
    template = 'index.html'
    if db_name is None:
        dbs = [db.get('NAME') for db in settings.DATABASES.itervalues()]
        ctx = {
            'dbs': dbs
        }
    else:
        ctx = {
            'url': reverse('db_wise_data', args=(db_name,))
        }
    return render(request, template, ctx)

def create_response(data):
    response = []
    for data_point in data:
	data_dict = {
		'timestamp': data_point.timestamp,
		'num_queries': data_point.num_queries,
		'average_query_time': data_point.average_query_time,
		'num_joined_queries': data_point.num_joined_queries,
	}
	data_dict['num_insert_queries'] = data_point.num_queries if data_point.query_type == 'INSERT' else 0
	data_dict['num_update_queries'] = data_point.num_queries if data_point.query_type == 'UPDATE' else 0
	data_dict['num_delete_queries'] = data_point.num_queries if data_point.query_type == 'DELETE' else 0
	data_dict['num_select_queries'] = data_point.num_queries if data_point.query_type == 'SELECT' else 0
	response.append(data_dict)
    response = json.dumps(response, cls=DjangoJSONEncoder)
    response = HttpResponse(response, content_type='application/json')
    return response


def get_app_wise_data(request, app_name):

    data = AppWiseAggregatedMetric.objects.filter(
            app_name=app_name).order_by('-timestamp')[:-40]
    return create_response(data)

def get_table_wise_data(request, table_name):

    data = TableWiseAggregatedMetric.objects.filter(
            table_name=table_name).order_by('-timestamp')[:40]
    return create_response(data)

def get_db_wise_data(request, db_name):
    data = DBWiseAggregatedMetric.objects.filter(
            db_name=db_name).order_by('-timestamp')[:40]
    return create_response(data)
