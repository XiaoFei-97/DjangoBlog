# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-09-19 15:58
from __future__ import unicode_literals

import DjangoUeditor.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import read_statistics.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='分类')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, verbose_name='文章标题')),
                ('body', DjangoUeditor.models.UEditorField(verbose_name='内容')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modified_time', models.DateTimeField(auto_now_add=True, verbose_name='修改时间')),
                ('excerpt', models.CharField(blank=True, max_length=200, verbose_name='摘要')),
                ('display', models.IntegerField(choices=[(0, '直接发表'), (1, '保留草稿')], null=True, verbose_name='是否发表')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Category', verbose_name='分类')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'ordering': ['-created_time'],
            },
            bases=(models.Model, read_statistics.models.ReadNumExpandMethod),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='标签')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='blog.Tag', verbose_name='标签'),
        ),
    ]
