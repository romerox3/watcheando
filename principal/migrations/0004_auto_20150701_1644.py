# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0003_auto_20150626_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoh',
            name='archivo',
            field=models.FileField(upload_to=b'media/videos', blank=True),
        ),
    ]
