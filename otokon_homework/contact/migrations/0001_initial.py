# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-23 10:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('homework', '0004_auto_20160623_1000'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('is_answered', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=100)),
                ('added_time', models.DateTimeField(auto_now_add=True)),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homework.Homework')),
                ('send_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Send', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Take', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
