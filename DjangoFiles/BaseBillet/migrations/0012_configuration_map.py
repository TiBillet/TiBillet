# Generated by Django 2.2 on 2021-11-10 03:40

from django.db import migrations
import stdimage.models
import stdimage.validators


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0011_configuration_button_adhesion'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='map',
            field=stdimage.models.StdImageField(blank=True, null=True, upload_to='images/', validators=[stdimage.validators.MaxSizeValidator(1920, 1920)], verbose_name='Carte géorgraphique'),
        ),
    ]
