# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-15 06:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_check_nag_after'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='nag_after',
            field=models.DateTimeField(null=True),
        ),
    ]
