from django.conf.urls import url


urlpatterns = [
    url(r'^$',
        'django_db_meter.views.index',
        name='index'
    ),
    url(r'^app-wise-data/(?P<app_name>\w+)/$',
        'django_db_meter.views.get_app_wise_data',
        name='app_wise_data'
    ),
    url(r'^table-wise-data/(?P<table_name>\w+)/$',
        'django_db_meter.views.get_table_wise_data',
        name='table_wise_data'
    ),
    url(r'^db-wise-data/(?P<db_name>\w+)/$',
        'django_db_meter.views.get_db_wise_data',
        name='db_wise_data'
    ),
    url(r'^apps/(?P<app_name>\w+)/$',
        'django_db_meter.views.list_apps',
        name='view_app'
    ),
    url(r'^apps/$',
        'django_db_meter.views.list_apps',
        name='list_apps'
    ),
    url(r'^tables/(?P<table_name>\w+)/$',
        'django_db_meter.views.list_tables',
        name='view_table'
    ),
    url(r'^tables/$',
        'django_db_meter.views.list_tables',
        name='list_tables'
    ),
    url(r'^dbs/(?P<db_name>\w+)/$',
        'django_db_meter.views.list_dbs',
        name='view_db'
    ),
    url(r'^dbs/$',
        'django_db_meter.views.list_dbs',
        name='list_dbs'
    ),
]
