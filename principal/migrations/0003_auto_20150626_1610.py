# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0002_auto_20150626_1609'),
    ]

    operations = [
        migrations.RenameField(
            model_name='videoh',
            old_name='imagen',
            new_name='archivo',
        ),
    ]
