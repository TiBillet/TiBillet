# Generated by Django 3.2 on 2022-05-05 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0008_auto_20220505_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='slug',
            field=models.SlugField(default='m'),
            preserve_default=False,
        ),
    ]
