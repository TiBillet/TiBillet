# Generated by Django 2.2 on 2021-11-09 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0008_auto_20211109_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='paiement_stripe',
            name='traitement_en_cours',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('C', 'Annulée'), ('R', 'Crée'), ('U', 'Non payée'), ('P', 'Payée'), ('PE', 'Payée mais mail non valide'), ('V', 'Validée')], default='R', max_length=3, verbose_name='Status de la réservation'),
        ),
    ]
