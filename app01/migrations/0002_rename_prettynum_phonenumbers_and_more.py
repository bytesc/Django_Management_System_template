# Generated by Django 4.2 on 2023-04-25 09:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="PrettyNum",
            new_name="PhoneNumbers",
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="creat_time",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(2023, 4, 25, 17, 30, 12, 789058),
                null=True,
                verbose_name="入职时间",
            ),
        ),
    ]
