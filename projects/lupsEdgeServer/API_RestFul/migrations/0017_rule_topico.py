# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-06-09 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API_RestFul', '0016_remove_rule_topico'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='topico',
            field=models.CharField(default=10, max_length=200),
            preserve_default=False,
        ),
    ]
