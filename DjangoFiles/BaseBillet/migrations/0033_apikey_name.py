# Generated by Django 3.2 on 2022-09-27 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0032_apikey_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikey',
            name='name',
            field=models.CharField(default='prou', max_length=30, unique=True),
            preserve_default=False,
        ),
    ]