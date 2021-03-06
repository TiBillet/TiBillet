# Generated by Django 3.2 on 2022-05-31 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0009_configuration_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='adhesion_obligatoire',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='adhesion_obligatoire', to='BaseBillet.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='categorie_article',
            field=models.CharField(choices=[('B', 'Billet'), ('P', "Pack d'objets"), ('R', 'Recharge cashless'), ('T', 'Vetement'), ('M', 'Merchandasing'), ('A', 'Adhésions et abonnements'), ('D', 'Don'), ('F', 'Reservation gratuite')], default='B', max_length=3, verbose_name="Type d'article"),
        ),
    ]
