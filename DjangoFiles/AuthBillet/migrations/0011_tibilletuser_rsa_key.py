# Generated by Django 4.2.10 on 2024-02-15 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AuthBillet', '0010_rsakey'),
    ]

    operations = [
        migrations.AddField(
            model_name='tibilletuser',
            name='rsa_key',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='AuthBillet.rsakey'),
        ),
    ]
