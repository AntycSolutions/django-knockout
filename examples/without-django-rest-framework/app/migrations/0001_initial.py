# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('day', models.DateField(verbose_name='Day')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=64, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=64, verbose_name='Last Name')),
            ],
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('reminder', models.CharField(max_length=32, verbose_name='Reminder')),
            ],
        ),
        migrations.CreateModel(
            name='ReminderType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('reminder_type', models.TextField(verbose_name='Reminder')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('task', models.TextField(verbose_name='Task')),
                ('day', models.ForeignKey(to='app.Day')),
                ('reminder', models.ForeignKey(to='app.Reminder')),
            ],
        ),
        migrations.AddField(
            model_name='reminder',
            name='reminder_type',
            field=models.ForeignKey(to='app.ReminderType'),
        ),
    ]
