# Generated by Django 2.2.12 on 2021-03-10 14:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0007_wxcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='wxcomment',
            name='comm_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='提交评论时间'),
        ),
        migrations.AlterField(
            model_name='wxcomment',
            name='counts',
            field=models.IntegerField(blank=True, null=True, verbose_name='评分'),
        ),
    ]