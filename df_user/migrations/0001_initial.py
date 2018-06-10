# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uname', models.CharField(max_length=20, verbose_name='\u7528\u6237\u540d')),
                ('upwd', models.CharField(max_length=40, verbose_name='\u5bc6\u7801')),
                ('uemail', models.CharField(max_length=30, verbose_name='\u7535\u5b50\u90ae\u7bb1')),
                ('ushow', models.CharField(default=b'', max_length=20, verbose_name='\u6536\u4ef6\u4eba\u540d\u5b57')),
                ('uaddress', models.CharField(default=b'', max_length=100, verbose_name='\u6536\u4ef6\u5730\u5740')),
                ('uyoubian', models.CharField(default=b'', max_length=6, verbose_name='\u6536\u4ef6\u90ae\u7f16')),
                ('uphone', models.CharField(default=b'', max_length=11, verbose_name='\u6536\u4ef6\u4eba\u7535\u8bdd')),
            ],
            options={
                'verbose_name_plural': '\u7528\u6237\u7ba1\u7406',
            },
        ),
    ]
