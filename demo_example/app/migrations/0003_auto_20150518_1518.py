# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150518_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='reminder',
            field=models.ForeignKey(null=True, to='app.Reminder'),
        ),
    ]
