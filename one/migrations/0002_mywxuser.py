# Generated by Django 2.2.12 on 2021-02-22 11:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='mywxuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(blank=True, max_length=500, null=True, verbose_name='微信openid')),
                ('nickname', models.CharField(blank=True, max_length=200, null=True, verbose_name='微信签名')),
                ('gender', models.CharField(blank=True, max_length=2, null=True, verbose_name='性别')),
                ('city', models.CharField(blank=True, max_length=200, null=True, verbose_name='城市')),
                ('province', models.CharField(blank=True, max_length=200, null=True, verbose_name='省')),
                ('country', models.CharField(blank=True, max_length=200, null=True, verbose_name='国家')),
                ('avatar', models.CharField(blank=True, max_length=2000, null=True, verbose_name='微信头像URL')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='手机号')),
                ('c_time', models.DateTimeField(auto_now=True, null=True, verbose_name='添加时间')),
                ('token', models.CharField(blank=True, max_length=3000, null=True)),
                ('expiration_time', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='过期时间')),
                ('add_time', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='token添加时间')),
            ],
        ),
    ]