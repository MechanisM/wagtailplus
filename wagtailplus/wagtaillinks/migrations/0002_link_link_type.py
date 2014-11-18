# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaillinks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='link_type',
            field=models.PositiveIntegerField(default=1, verbose_name='Link Type', editable=False),
            preserve_default=False,
        ),
    ]
