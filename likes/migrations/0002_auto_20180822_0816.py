# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-08-22 08:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='likecount',
            options={'ordering': ['-liked_num'], 'verbose_name': '点赞计数', 'verbose_name_plural': '点赞计数'},
        ),
    ]