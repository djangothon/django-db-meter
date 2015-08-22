# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DBQueryMetric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('query_start_time', models.DateTimeField()),
                ('query_execution_time', models.FloatField(default=0.0)),
                ('query_sql', models.TextField()),
                ('query_tables', models.TextField()),
                ('db_name', models.CharField(max_length=255)),
                ('app_name', models.CharField(max_length=255)),
                ('rows_affected', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
