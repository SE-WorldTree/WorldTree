# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-09 09:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relation', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='edge',
            old_name='patid',
            new_name='pntid',
        ),
        migrations.RemoveField(
            model_name='vertex',
            name='usrID',
        ),
    ]