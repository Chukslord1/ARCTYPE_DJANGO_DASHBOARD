# Generated by Django 3.1.7 on 2021-05-02 16:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_auto_20210502_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editprofileevent',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 2, 17, 18, 17, 987848)),
        ),
        migrations.AlterField(
            model_name='event',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 2, 17, 18, 17, 986838)),
        ),
        migrations.AlterField(
            model_name='loginevent',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 2, 17, 18, 17, 987848)),
        ),
        migrations.AlterField(
            model_name='logoutevent',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 2, 17, 18, 17, 987848)),
        ),
        migrations.AlterField(
            model_name='registerevent',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 2, 17, 18, 17, 987848)),
        ),
        migrations.AlterField(
            model_name='viewpageevent',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 2, 17, 18, 17, 987848)),
        ),
    ]
