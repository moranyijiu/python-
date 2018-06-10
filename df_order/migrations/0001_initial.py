# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
        ('df_goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetailInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(verbose_name='\u4ef7\u94b1', max_digits=5, decimal_places=2)),
                ('count', models.IntegerField(verbose_name='\u6570\u91cf')),
                ('goods', models.ForeignKey(to='df_goods.GoodsInfo')),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('oid', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('odate', models.DateTimeField(auto_now=True, verbose_name='\u8d2d\u4e70\u65e5\u671f')),
                ('oIsPay', models.BooleanField(default=False, verbose_name='\u662f\u5426\u4ed8\u6b3e')),
                ('ototal', models.DecimalField(verbose_name='\u603b\u4ef7', max_digits=6, decimal_places=2)),
                ('oaddress', models.CharField(max_length=150, verbose_name='\u6536\u8d27\u5730\u5740')),
                ('user', models.ForeignKey(to='df_user.UserInfo')),
            ],
            options={
                'verbose_name_plural': '\u8ba2\u5355\u7ba1\u7406',
            },
        ),
        migrations.AddField(
            model_name='orderdetailinfo',
            name='order',
            field=models.ForeignKey(to='df_order.OrderInfo'),
        ),
    ]
