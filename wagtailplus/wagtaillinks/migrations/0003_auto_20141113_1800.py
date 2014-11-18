# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaillinks', '0002_link_link_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='email',
            field=models.EmailField(null=True, max_length=75, blank=True, help_text='Enter a valid email address', unique=True, verbose_name='Email'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='link',
            name='external_url',
            field=models.URLField(null=True, blank=True, help_text='Enter a valid URL, including scheme (e.g. http://)', unique=True, verbose_name='URL'),
            preserve_default=True,
        ),
    ]
