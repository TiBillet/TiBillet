# Generated by Django 2.2 on 2021-11-11 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QrcodeCashless', '0002_cartecashless_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='origine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='origine', to='Customers.Client'),
        ),
    ]