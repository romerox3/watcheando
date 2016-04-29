# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoh',
            name='careta',
            field=models.ImageField(upload_to=b'media/imagenes', blank=True),
        ),
        migrations.AlterField(
            model_name='videoh',
            name='imagen',
            field=models.FileField(upload_to=b'/media/videos', blank=True),
        ),
    ]
