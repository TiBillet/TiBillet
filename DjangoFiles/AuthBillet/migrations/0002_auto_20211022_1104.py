# Generated by Django 2.2 on 2021-10-22 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthBillet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tibilletuser',
            name='username',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]