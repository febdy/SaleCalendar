# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-08 09:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadshops', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roadshops',
            name='end_date',
            field=models.DateField(blank='', null=True),
        ),
        migrations.AlterField(
            model_name='roadshops',
            name='start_date',
            field=models.DateField(blank='', null=True),
        ),
    ]
