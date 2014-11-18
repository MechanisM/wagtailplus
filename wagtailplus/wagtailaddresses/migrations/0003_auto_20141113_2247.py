# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailaddresses', '0002_address_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='admin_level_1',
            field=models.ForeignKey(related_name='+', verbose_name='State', to='wagtailaddresses.AddressComponent'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='address',
            name='admin_level_2',
            field=models.ForeignKey(related_name='+', verbose_name='County', blank=True, to='wagtailaddresses.AddressComponent', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.ForeignKey(related_name='+', verbose_name='Country', to='wagtailaddresses.AddressComponent'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='address',
            name='locality',
            field=models.ForeignKey(related_name='+', verbose_name='City', to='wagtailaddresses.AddressComponent'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='address',
            name='postal_code',
            field=models.ForeignKey(related_name='+', verbose_name='Postal Code', to='wagtailaddresses.AddressComponent'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='address',
            name='route',
            field=models.ForeignKey(related_name='+', verbose_name='Street Name', to='wagtailaddresses.AddressComponent'),
            preserve_default=True,
        ),
    ]
