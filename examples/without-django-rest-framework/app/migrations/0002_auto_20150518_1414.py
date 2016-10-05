# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remindertype',
            name='reminder_type',
            field=models.CharField(max_length=32, verbose_name='Reminder'),
        ),
    ]
