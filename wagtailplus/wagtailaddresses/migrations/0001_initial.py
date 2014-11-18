# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailadmin.taggable
import taggit.managers
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Geometry', null=True, editable=False, blank=True)),
                ('label', models.CharField(verbose_name='Label', unique=True, max_length=200, editable=False)),
                ('street_number', models.CharField(max_length=6, verbose_name='Street Number', db_index=True)),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
            bases=(models.Model, wagtail.wagtailadmin.taggable.TagSearchable),
        ),
        migrations.CreateModel(
            name='AddressComponent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=50, verbose_name='Component Type', db_index=True)),
                ('short_name', models.CharField(max_length=255, verbose_name='Short Name', db_index=True)),
                ('long_name', models.CharField(max_length=255, verbose_name='Long Name', db_index=True)),
            ],
            options={
                'ordering': ('long_name',),
            },
            bases=(models.Model, wagtail.wagtailadmin.taggable.TagSearchable),
        ),
        migrations.AlterUniqueTogether(
            name='addresscomponent',
            unique_together=set([('type', 'long_name'), ('type', 'short_name')]),
        ),
        migrations.AddField(
            model_name='address',
            name='admin_level_1',
            field=models.ForeignKey(related_name='+', verbose_name='State', to='wagtailaddresses.AddressComponent', help_text='Select the 1st-level administrative area component for this address.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='admin_level_2',
            field=models.ForeignKey(related_name='+', blank=True, to='wagtailaddresses.AddressComponent', help_text='Select the 2nd-level administrative area component for this address.', null=True, verbose_name='County'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.ForeignKey(related_name='+', verbose_name='Country', to='wagtailaddresses.AddressComponent', help_text='Select the country component for this address.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='locality',
            field=models.ForeignKey(related_name='+', verbose_name='City', to='wagtailaddresses.AddressComponent', help_text='Select the locality component for this address.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='postal_code',
            field=models.ForeignKey(related_name='+', verbose_name='Postal Code', to='wagtailaddresses.AddressComponent', help_text='Select the postal code component for this address.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='route',
            field=models.ForeignKey(related_name='+', verbose_name='Street Name', to='wagtailaddresses.AddressComponent', help_text='Select the route component for this address.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text=None, verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set([('street_number', 'route', 'postal_code')]),
        ),
    ]
