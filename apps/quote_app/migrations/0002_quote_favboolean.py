# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-25 18:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='favBoolean',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]