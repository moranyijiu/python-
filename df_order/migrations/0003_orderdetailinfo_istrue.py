# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_order', '0002_auto_20171218_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetailinfo',
            name='isTrue',
            field=models.BooleanField(default=False),
        ),
    ]
