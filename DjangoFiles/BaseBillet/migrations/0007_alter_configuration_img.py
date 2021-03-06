# Generated by Django 3.2 on 2022-05-03 08:40

from django.db import migrations
import stdimage.models
import stdimage.validators


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0006_auto_20220428_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='img',
            field=stdimage.models.StdImageField(upload_to='images/', validators=[stdimage.validators.MinSizeValidator(720, 720)], verbose_name='Background'),
        ),
    ]
