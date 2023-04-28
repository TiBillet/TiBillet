# Generated by Django 3.2 on 2023-01-11 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0002_alter_client_categorie'),
        ('QrcodeCashless', '0009_federatedcashless_syncfederatedlog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='federated_with',
        ),
        migrations.AlterUniqueTogether(
            name='federatedcashless',
            unique_together={('client', 'asset')},
        ),
    ]