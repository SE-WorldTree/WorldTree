# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-07 12:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='edge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pntid', models.IntegerField()),
                ('chdid', models.IntegerField()),
                ('beginDate', models.DateField()),
                ('endDate', models.DateField()),
                ('cnt', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('isusr', models.BooleanField()),
                ('uid', models.IntegerField()),
                ('email', models.EmailField(max_length=50)),
                ('nickname', models.CharField(max_length=50)),
                ('blog', models.CharField(max_length=50)),
                ('linkedin', models.CharField(max_length=50)),
                ('ggsc', models.CharField(max_length=50)),
            ],
        ),
    ]
