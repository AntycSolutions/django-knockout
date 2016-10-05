# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_item_shopping'),
    ]

    operations = [
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('description', models.TextField(verbose_name='Description')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.ForeignKey(null=True, to='app.Description', blank=True),
        ),
    ]
