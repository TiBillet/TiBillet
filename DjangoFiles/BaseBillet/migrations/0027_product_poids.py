# Generated by Django 3.2 on 2022-08-12 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0026_alter_configuration_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='poids',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Poids'),
        ),
    ]
