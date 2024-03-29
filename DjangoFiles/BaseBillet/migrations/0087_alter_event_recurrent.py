# Generated by Django 3.2 on 2023-11-03 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0086_auto_20230908_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='recurrent',
            field=models.ManyToManyField(blank=True, help_text="Selectionnez le jour de la semaine pour une récurence hebdomadaire. La date de l'évènement sera la date de fin de la récurence.", to='BaseBillet.Weekday', verbose_name='Jours de la semaine'),
        ),
    ]
