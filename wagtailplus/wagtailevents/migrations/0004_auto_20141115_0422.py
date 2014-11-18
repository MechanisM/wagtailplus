# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailevents', '0003_auto_20141114_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(unique=True, max_length=100, verbose_name='Name'),
            preserve_default=True,
        ),
    ]
