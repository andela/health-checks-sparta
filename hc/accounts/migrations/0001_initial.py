# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-26 08:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checks', models.ManyToManyField(to='api.Check')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(blank=True, max_length=200)),
                ('team_access_allowed', models.BooleanField(default=False)),
                ('next_report_date', models.DateTimeField(blank=True, null=True)),
                ('daily_reports_allowed', models.BooleanField(default=False)),
                ('monthly_reports_allowed', models.BooleanField(default=True)),
                ('weekly_reports_allowed', models.BooleanField(default=False)),
                ('ping_log_limit', models.IntegerField(default=100)),
                ('token', models.CharField(blank=True, max_length=128)),
                ('api_key', models.CharField(blank=True, max_length=128)),
                ('current_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile'),
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
