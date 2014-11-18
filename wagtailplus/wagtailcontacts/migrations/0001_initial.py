# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models
import django.db.models.deletion
import taggit.managers
import wagtail.wagtailadmin.taggable


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0004_make_focal_point_key_not_nullable'),
        ('wagtailaddresses', '0002_address_created_at'),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(help_text='Enter a name for this contact', max_length=100, verbose_name='Name', db_index=True)),
                ('website', models.URLField(help_text='Enter an optional website for this contact', null=True, verbose_name='Website', blank=True)),
                ('email', models.EmailField(help_text='Enter an optional email address for this contact', max_length=75, null=True, verbose_name='Email', blank=True)),
                ('telephone', localflavor.us.models.PhoneNumberField(help_text='Enter an optional telephone number for this contact', max_length=20, null=True, verbose_name='Telephone', blank=True)),
                ('address', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailaddresses.Address', help_text='Select an optional address for this contact', null=True)),
                ('image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', help_text='Select an optional image for this contact', null=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text=None, verbose_name='Tags')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
            bases=(models.Model, wagtail.wagtailadmin.taggable.TagSearchable),
        ),
        migrations.AlterUniqueTogether(
            name='contact',
            unique_together=set([('name', 'email'), ('name', 'website')]),
        ),
    ]
