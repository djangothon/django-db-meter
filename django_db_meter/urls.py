from django.conf.urls import url


urlpatterns = [
    url(r'^app-wise-data/(?P<app_name>)\w+/$',
        'django_db_meter.views.get_app_wise_data',
        name='app_wise_data'
    )
]
