# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-22 20:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0002_auto_20180821_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('NW', 'New'), ('UR', 'Under Review'), ('DE', 'Declined'), ('NM', 'Needs More Info'), ('PD', 'Planned'), ('IP', 'In Progress'), ('CP', 'Completed')], default='NW', max_length=2),
        ),
        migrations.DeleteModel(
            name='IssueStatus',
        ),
    ]
