# Generated by Django 3.2 on 2023-03-31 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0057_auto_20230102_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paiement_stripe',
            name='status',
            field=models.CharField(choices=[('N', 'Lien de paiement non créé'), ('O', 'Envoyée a Stripe'), ('W', 'En attente de paiement'), ('E', 'Expiré'), ('P', 'Payée'), ('V', 'Payée et validée'), ('S', 'Payée mais problème de synchro cashless'), ('C', 'Annulée')], default='N', max_length=1, verbose_name='Statut de la commande'),
        ),
    ]
