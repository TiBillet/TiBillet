# Generated by Django 3.2 on 2022-06-25 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0020_membership_stripe_id_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='paiement_stripe',
            name='invoice_stripe',
            field=models.CharField(blank=True, max_length=27, null=True),
        ),
    ]
