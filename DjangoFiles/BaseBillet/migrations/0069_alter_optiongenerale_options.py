# Generated by Django 3.2 on 2023-04-28 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0068_auto_20230427_1826'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='optiongenerale',
            options={'ordering': ('poids',), 'verbose_name': 'Option', 'verbose_name_plural': 'Options'},
        ),
    ]
