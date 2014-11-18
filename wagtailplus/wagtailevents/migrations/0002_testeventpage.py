# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailevents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestEventPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(help_text='Leave blank if these are the default details for this event.', null=True, verbose_name='Date', db_index=True, blank=True)),
                ('start', models.TimeField(db_index=True, null=True, verbose_name='Start Time', blank=True)),
                ('end', models.TimeField(null=True, verbose_name='End Time', blank=True)),
                ('event', models.ForeignKey(related_name='pages', to='wagtailevents.Event')),
            ],
            options={
                'ordering': ('start',),
                'abstract': False,
                'verbose_name': 'Event Page',
                'verbose_name_plural': 'Event Pages',
            },
            bases=(models.Model,),
        ),
    ]
