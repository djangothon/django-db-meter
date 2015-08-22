# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_db_meter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppWiseAggregatedMetric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('num_queries', models.PositiveIntegerField(default=0)),
                ('average_query_time', models.FloatField(default=0.0)),
                ('num_joined_queries', models.PositiveIntegerField(default=0)),
                ('app_name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DBWiseAggregatedMetric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('num_queries', models.PositiveIntegerField(default=0)),
                ('average_query_time', models.FloatField(default=0.0)),
                ('num_joined_queries', models.PositiveIntegerField(default=0)),
                ('db_name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TableWiseAggregatedMetric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('num_queries', models.PositiveIntegerField(default=0)),
                ('average_query_time', models.FloatField(default=0.0)),
                ('num_joined_queries', models.PositiveIntegerField(default=0)),
                ('table_name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
