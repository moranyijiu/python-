# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0001_initial'),
        ('df_order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='sales',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField(verbose_name='\u9500\u91cf')),
                ('totalprice', models.DecimalField(verbose_name='\u9500\u552e\u989d', max_digits=5, decimal_places=2)),
                ('goods', models.ForeignKey(to='df_goods.GoodsInfo')),
            ],
        ),
        migrations.AlterModelOptions(
            name='orderdetailinfo',
            options={'verbose_name_plural': '\u53d1\u8d27\u7ba1\u7406'},
        ),
    ]
