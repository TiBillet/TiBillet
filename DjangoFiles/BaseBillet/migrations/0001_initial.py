# Generated by Django 3.2 on 2022-02-09 13:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import stdimage.models
import stdimage.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('QrcodeCashless', '0001_initial'),
        ('Customers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
                ('datetime', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('short_description', models.CharField(blank=True, max_length=250, null=True)),
                ('long_description', models.TextField(blank=True, null=True)),
                ('event_facebook_url', models.URLField(blank=True, null=True)),
                ('published', models.BooleanField(default=False)),
                ('img', stdimage.models.StdImageField(blank=True, null=True, upload_to='images/', validators=[stdimage.validators.MaxSizeValidator(1920, 1920)])),
                ('categorie', models.CharField(choices=[('LIV', 'Concert'), ('FES', 'Festival'), ('REU', 'Réunion'), ('CON', 'Conférence')], default='LIV', max_length=3, verbose_name="Catégorie d'évènement")),
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
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
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
            name='Price',
            fields=[
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('prix', models.FloatField()),
                ('vat', models.CharField(choices=[('NA', 'Non applicable'), ('DX', '10 %'), ('VG', '20 %')], default='NA', max_length=2, verbose_name='Taux TVA')),
                ('stock', models.SmallIntegerField(blank=True, null=True)),
                ('max_per_user', models.PositiveSmallIntegerField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name='PriceSold',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('id_price_stripe', models.CharField(blank=True, max_length=30, null=True)),
                ('qty_solded', models.SmallIntegerField(default=0)),
                ('prix', models.FloatField()),
                ('price', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BaseBillet.price')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=500, unique=True)),
                ('publish', models.BooleanField(default=False)),
                ('img', stdimage.models.StdImageField(blank=True, null=True, upload_to='images/', validators=[stdimage.validators.MaxSizeValidator(1920, 1920)], verbose_name='Image du produit')),
                ('categorie_article', models.CharField(choices=[('B', 'Billet'), ('P', "Pack d'objets"), ('R', 'Recharge cashless'), ('T', 'Vetement'), ('M', 'Merchandasing'), ('A', 'Adhésion')], default='B', max_length=3, verbose_name="Type d'article")),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('C', 'Annulée'), ('R', 'Crée'), ('U', 'Non payée'), ('P', 'Payée'), ('PE', 'Payée mais mail non valide'), ('V', 'Validée')], default='R', max_length=3, verbose_name='Status de la réservation')),
                ('mail_send', models.BooleanField(default=False)),
                ('mail_error', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reservation', to='BaseBillet.event')),
                ('options', models.ManyToManyField(blank=True, to='BaseBillet.OptionGenerale')),
                ('user_commande', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-datetime',),
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('C', 'Crée'), ('N', 'Non actif'), ('K', 'Non scanné'), ('S', 'scanné')], default='C', max_length=1, verbose_name='Status du scan')),
                ('seat', models.CharField(default='Placement libre', max_length=20)),
                ('pricesold', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BaseBillet.pricesold')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='BaseBillet.reservation')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSold',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('id_product_stripe', models.CharField(blank=True, max_length=30, null=True)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='BaseBillet.event')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BaseBillet.product')),
            ],
        ),
        migrations.AddField(
            model_name='pricesold',
            name='productsold',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BaseBillet.productsold'),
        ),
        migrations.AddField(
            model_name='price',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='prices', to='BaseBillet.product'),
        ),
        migrations.CreateModel(
            name='Paiement_stripe',
            fields=[
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('detail', models.CharField(blank=True, max_length=50, null=True)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('checkout_session_id_stripe', models.CharField(blank=True, max_length=80, null=True)),
                ('payment_intent_id', models.CharField(blank=True, max_length=80, null=True)),
                ('metadata_stripe', models.JSONField(blank=True, null=True)),
                ('order_date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('last_action', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('N', 'Lien de paiement non créé'), ('O', 'Envoyée a Stripe'), ('W', 'En attente de paiement'), ('E', 'Expiré'), ('P', 'Payée'), ('V', 'Payée et validée'), ('C', 'Annulée')], default='N', max_length=1, verbose_name='Statut de la commande')),
                ('traitement_en_cours', models.BooleanField(default=False)),
                ('source_traitement', models.CharField(choices=[('N', 'Pas de traitement en cours'), ('W', 'Depuis webhook post stripe'), ('G', 'Depuis Get')], default='N', max_length=1, verbose_name='Source de la commande')),
                ('source', models.CharField(choices=[('Q', 'Depuis scan QR-Code'), ('B', 'Depuis billetterie')], default='B', max_length=1, verbose_name='Source de la commande')),
                ('total', models.FloatField(default=0)),
                ('reservation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='paiements', to='BaseBillet.reservation')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LigneArticle',
            fields=[
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('qty', models.SmallIntegerField()),
                ('status', models.CharField(choices=[('C', 'Annulée'), ('O', 'Non envoyé en paiement'), ('U', 'Non payée'), ('P', 'Payée'), ('V', 'Validée par serveur cashless')], default='O', max_length=3, verbose_name='Status de ligne article')),
                ('carte', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='QrcodeCashless.cartecashless')),
                ('paiement_stripe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='BaseBillet.paiement_stripe')),
                ('pricesold', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BaseBillet.pricesold')),
            ],
            options={
                'ordering': ('-datetime',),
            },
        ),
        migrations.AddField(
            model_name='event',
            name='products',
            field=models.ManyToManyField(blank=True, to='BaseBillet.Product'),
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisation', models.CharField(db_index=True, max_length=50, verbose_name="Nom de l'organisation")),
                ('short_description', models.CharField(max_length=250, verbose_name='Description courte')),
                ('long_description', models.TextField(blank=True, null=True)),
                ('adress', models.CharField(blank=True, max_length=250, null=True)),
                ('postal_code', models.IntegerField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=250, null=True)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('site_web', models.URLField(blank=True, null=True)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('facebook', models.URLField(blank=True, null=True)),
                ('instagram', models.URLField(blank=True, null=True)),
                ('adhesion_obligatoire', models.BooleanField(default=False)),
                ('button_adhesion', models.BooleanField(default=False)),
                ('map_img', stdimage.models.StdImageField(blank=True, null=True, upload_to='images/', validators=[stdimage.validators.MaxSizeValidator(1920, 1920)], verbose_name='Carte géorgraphique')),
                ('carte_restaurant', stdimage.models.StdImageField(blank=True, null=True, upload_to='images/', validators=[stdimage.validators.MaxSizeValidator(1920, 1920)], verbose_name='Carte du restaurant')),
                ('img', stdimage.models.StdImageField(upload_to='images/', validators=[stdimage.validators.MaxSizeValidator(1920, 1920), stdimage.validators.MinSizeValidator(720, 720)], verbose_name='Background')),
                ('logo', stdimage.models.StdImageField(upload_to='images/', validators=[stdimage.validators.MaxSizeValidator(1920, 1920)], verbose_name='Logo')),
                ('mollie_api_key', models.CharField(blank=True, max_length=50, null=True)),
                ('stripe_api_key', models.CharField(blank=True, default='', max_length=110, null=True)),
                ('stripe_test_api_key', models.CharField(blank=True, default='sk_test_51Jcl7GDGhGI7kQoo5uzjfL9HFQD7ZWfnWbBK6NvEYA4Wn0tsE4z2PCriZVRe3n95FZs2iDUDUkvwdRgOV5frYEi1009NpnRV25', max_length=110, null=True)),
                ('stripe_mode_test', models.BooleanField(default=True)),
                ('activer_billetterie', models.BooleanField(default=True, verbose_name='Activer la billetterie')),
                ('jauge_max', models.PositiveSmallIntegerField(default=50, verbose_name='Jauge maximale')),
                ('server_cashless', models.URLField(blank=True, max_length=300, null=True, verbose_name='Adresse du serveur Cashless')),
                ('key_cashless', models.CharField(blank=True, max_length=41, null=True, verbose_name="Clé d'API du serveur cashless")),
                ('template_billetterie', models.CharField(blank=True, choices=[('arnaud_mvc', 'arnaud_mvc'), ('html5up-masseively', 'html5up-masseively'), ('blk-pro-mvc', 'blk-pro-mvc')], default='arnaud_mvc', max_length=250, null=True, verbose_name='Template Billetterie')),
                ('template_meta', models.CharField(blank=True, choices=[('arnaud_mvc', 'arnaud_mvc'), ('html5up-masseively', 'html5up-masseively'), ('blk-pro-mvc', 'blk-pro-mvc')], default='html5up-masseively', max_length=250, null=True, verbose_name='Template Meta')),
                ('option_generale_checkbox', models.ManyToManyField(blank=True, related_name='checkbox', to='BaseBillet.OptionGenerale')),
                ('option_generale_radio', models.ManyToManyField(blank=True, related_name='radiobutton', to='BaseBillet.OptionGenerale')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Artist_on_event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Customers.client')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artists', to='BaseBillet.event')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='price',
            unique_together={('name', 'product')},
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together={('name', 'datetime')},
        ),
    ]
