# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaillinks', '0003_auto_20141113_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='email',
            field=models.EmailField(help_text='Enter a valid email address', max_length=75, null=True, verbose_name='Email', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='link',
            name='external_url',
            field=models.URLField(help_text='Enter a valid URL, including scheme (e.g. http://)', null=True, verbose_name='URL', blank=True),
            preserve_default=True,
        ),
    ]
