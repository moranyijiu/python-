# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gtitle', models.CharField(max_length=20, verbose_name='\u540d\u5b57')),
                ('gpic', models.ImageField(upload_to=b'df_goods', verbose_name='\u56fe\u7247')),
                ('gprice', models.DecimalField(verbose_name='\u4ef7\u94b1', max_digits=5, decimal_places=2)),
                ('isDelete', models.BooleanField(default=False)),
                ('gunit', models.CharField(default=b'500g', max_length=20, verbose_name='\u5355\u4f4d')),
                ('gclick', models.IntegerField(verbose_name='\u70b9\u51fb')),
                ('gjianjie', models.CharField(max_length=200)),
                ('gkucun', models.IntegerField(verbose_name='\u5e93\u5b58')),
                ('gcontent', tinymce.models.HTMLField(verbose_name='\u63cf\u8ff0')),
            ],
            options={
                'verbose_name_plural': '\u6c34\u679c',
            },
        ),
        migrations.CreateModel(
            name='TypeInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ttitle', models.CharField(max_length=20, verbose_name='\u79cd\u7c7b')),
                ('isDelete', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': '\u6c34\u679c\u7c7b\u578b\u4fee\u6539',
            },
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='gtype',
            field=models.ForeignKey(to='df_goods.TypeInfo'),
        ),
    ]
