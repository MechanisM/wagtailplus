# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailaddresses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Geometry', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
