# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailaddresses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 10, 17, 35, 45, 367142, tzinfo=utc), verbose_name='Created', auto_now_add=True),
            preserve_default=False,
        ),
    ]
