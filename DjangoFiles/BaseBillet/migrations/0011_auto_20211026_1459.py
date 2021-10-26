# Generated by Django 2.2 on 2021-10-26 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0010_auto_20211025_1002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lignearticle',
            name='reservation',
        ),
        migrations.AlterField(
            model_name='configuration',
            name='name_required_for_ticket',
            field=models.BooleanField(default=False, verbose_name='Billet nominatifs'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='scan_status',
            field=models.CharField(choices=[('N', 'Non actif'), ('K', 'Non scanné'), ('S', 'scanné')], default='N', max_length=1, verbose_name='Status du scan'),
        ),
    ]