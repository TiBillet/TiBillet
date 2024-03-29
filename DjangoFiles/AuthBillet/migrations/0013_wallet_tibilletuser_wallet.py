# Generated by Django 4.2.10 on 2024-02-16 13:09

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('AuthBillet', '0012_alter_tibilletuser_rsa_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='tibilletuser',
            name='wallet',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='AuthBillet.wallet'),
        ),
    ]
