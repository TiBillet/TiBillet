# Generated by Django 2.2 on 2021-06-23 09:09

from django.db import migrations, models
import django.db.models.deletion
import stdimage.models
import stdimage.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('short_description', models.CharField(max_length=250)),
                ('long_description', models.TextField(blank=True, null=True)),
                ('datetime', models.DateTimeField()),
                ('img', stdimage.models.StdImageField(blank=True, null=True, upload_to='images/', validators=[stdimage.validators.MaxSizeValidator(1920, 1920)])),
                ('reservations', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Evenement',
                'verbose_name_plural': 'Evenements',
                'ordering': ('datetime',),
            },
        ),
        migrations.CreateModel(
            name='OptionGenerale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('poids', models.PositiveSmallIntegerField(default=0, verbose_name='Poids')),
            ],
            options={
                'verbose_name': 'Options Generales',
                'verbose_name_plural': 'Options Generales',
                'ordering': ('poids',),
            },
        ),
        migrations.CreateModel(
            name='reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('NAN', 'Annulée'), ('NOV', 'Email non validé'), ('VAL', 'Validée'), ('PAY', 'Payée')], default='NOV', max_length=3, verbose_name='Status de la réservation')),
                ('qty', models.IntegerField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation', to='BaseBillet.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisation', models.CharField(max_length=50)),
                ('short_description', models.CharField(max_length=250)),
                ('adresse', models.CharField(max_length=250)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('facebook', models.URLField(blank=True, null=True)),
                ('instagram', models.URLField(blank=True, null=True)),
                ('img', stdimage.models.StdImageField(blank=True, null=True, upload_to='images/')),
                ('mollie_api_key', models.CharField(blank=True, max_length=50, null=True)),
                ('reservation_par_user_max', models.PositiveSmallIntegerField(default=6)),
                ('jauge_max', models.PositiveSmallIntegerField(default=50)),
                ('option_generale_checkbox', models.ManyToManyField(blank=True, related_name='checkbox', to='BaseBillet.OptionGenerale')),
                ('option_generale_radio', models.ManyToManyField(blank=True, related_name='radiobutton', to='BaseBillet.OptionGenerale')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
