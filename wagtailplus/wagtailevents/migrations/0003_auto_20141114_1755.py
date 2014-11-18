# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailevents', '0002_testeventpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testeventpage',
            name='event',
        ),
        migrations.DeleteModel(
            name='TestEventPage',
        ),
    ]
