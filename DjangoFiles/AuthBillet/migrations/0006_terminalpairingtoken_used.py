# Generated by Django 3.2 on 2022-04-22 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthBillet', '0005_auto_20220422_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='terminalpairingtoken',
            name='used',
            field=models.BooleanField(default=False),
        ),
    ]
