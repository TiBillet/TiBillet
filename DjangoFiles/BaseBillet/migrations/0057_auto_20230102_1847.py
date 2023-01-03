# Generated by Django 3.2 on 2023-01-02 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0056_pricesold_gift'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=500, verbose_name='Nom'),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('categorie_article', 'name')},
        ),
    ]
