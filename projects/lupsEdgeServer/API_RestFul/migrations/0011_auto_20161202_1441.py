# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-12-02 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API_RestFul', '0010_schedule_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='event',
            field=models.CharField(choices=[('gathering', 'Gather'), ('proceeding', 'Act'), ('publisher', 'Publish')], max_length=30, null=True),
        ),
    ]
