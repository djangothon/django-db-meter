# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_db_meter', '0003_testmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='appwiseaggregatedmetric',
            name='query_type',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='dbquerymetric',
            name='query_type',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='dbwiseaggregatedmetric',
            name='query_type',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='tablewiseaggregatedmetric',
            name='query_type',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
