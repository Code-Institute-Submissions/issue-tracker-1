# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-21 23:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='issuecategory',
            options={'verbose_name_plural': 'issue categories'},
        ),
        migrations.AlterModelOptions(
            name='issuestatus',
            options={'verbose_name_plural': 'issue statuses'},
        ),
        migrations.AddField(
            model_name='issue',
            name='status',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='issues.IssueStatus'),
            preserve_default=False,
        ),
    ]
