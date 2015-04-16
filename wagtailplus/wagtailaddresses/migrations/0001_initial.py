# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailadmin.taggable
import django.contrib.gis.db.models.fields
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(default=b'', verbose_name='Geometry', srid=4326, editable=False, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
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
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text=None, verbose_name='Tags')),
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
            name='administrative_area_level_1',
            field=models.ForeignKey(related_name='+', verbose_name='State', to='wagtailaddresses.AddressComponent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='administrative_area_level_2',
            field=models.ForeignKey(related_name='+', verbose_name='County', blank=True, to='wagtailaddresses.AddressComponent', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.ForeignKey(related_name='+', verbose_name='Country', to='wagtailaddresses.AddressComponent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='locality',
            field=models.ForeignKey(related_name='+', verbose_name='City', to='wagtailaddresses.AddressComponent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='postal_code',
            field=models.ForeignKey(related_name='+', verbose_name='Postal Code', to='wagtailaddresses.AddressComponent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='route',
            field=models.ForeignKey(related_name='+', verbose_name='Street Name', to='wagtailaddresses.AddressComponent'),
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
