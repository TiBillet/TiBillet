# Generated by Django 3.2 on 2023-01-25 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QrcodeCashless', '0012_syncfederatedlog_categorie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='syncfederatedlog',
            name='asset',
        ),
        migrations.AddField(
            model_name='syncfederatedlog',
            name='wallet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='QrcodeCashless.wallet'),
        ),
    ]
