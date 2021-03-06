# Generated by Django 3.2 on 2022-04-07 15:16

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_tenants.postgresql_backend.base
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('schema_name', models.CharField(db_index=True, max_length=63, unique=True, validators=[django_tenants.postgresql_backend.base._check_schema_name])),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('paid_until', models.DateField(default=django.utils.timezone.now)),
                ('on_trial', models.BooleanField(default=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('categorie', models.CharField(choices=[('A', 'Artiste'), ('S', 'Lieu de spectacle vivant'), ('F', 'Festival'), ('T', 'Tourneur'), ('P', 'Producteur'), ('M', 'Agenda culturel')], default='S', max_length=3, verbose_name='Categorie')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=253, unique=True)),
                ('is_primary', models.BooleanField(db_index=True, default=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='Customers.client')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
