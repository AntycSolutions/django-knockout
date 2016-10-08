# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('day', models.DateField(verbose_name='Day')),
            ],
        ),
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('description', models.TextField(verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name', max_length=64)),
                ('description', models.ForeignKey(to='app.Description', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('first_name', models.CharField(verbose_name='First Name', max_length=64)),
                ('last_name', models.CharField(verbose_name='Last Name', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('reminder', models.CharField(verbose_name='Reminder', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='ReminderType',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('reminder_type', models.CharField(verbose_name='Reminder', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Shopping',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name', max_length=32)),
                ('items', models.ManyToManyField(to='app.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('task', models.TextField(verbose_name='Task')),
                ('day', models.ForeignKey(to='app.Day')),
                ('reminder', models.ForeignKey(to='app.Reminder', blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='reminder',
            name='reminder_type',
            field=models.ForeignKey(to='app.ReminderType'),
        ),
    ]
