# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-02 03:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0005_auto_20180901_0124'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='issue',
            options={'ordering': ['-updated']},
        ),
        migrations.AlterField(
            model_name='issue',
            name='completed',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('NW', 'new'), ('UR', 'under-review'), ('DE', 'declined'), ('NM', 'needs-more-info'), ('PD', 'planned'), ('IP', 'in-progress'), ('CP', 'completed')], default='NW', max_length=2),
        ),
        migrations.AlterField(
            model_name='issue',
            name='updated',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]
