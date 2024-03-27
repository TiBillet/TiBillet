from django.utils import timezone

from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.utils.translation import gettext_lazy as _
import uuid

class Client(TenantMixin):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True)

    name = models.CharField(max_length=100, unique=True, db_index=True)
    paid_until =  models.DateField(default=timezone.now)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    ARTISTE, SALLE_SPECTACLE, FESTIVAL, TOURNEUR, PRODUCTEUR, META, ROOT = 'A', 'S', 'F', 'T', 'P', 'M', 'R'
    CATEGORIE_CHOICES = [
        (ARTISTE, _('Artiste')),
        (SALLE_SPECTACLE, _("Lieu de spectacle vivant")),
        (FESTIVAL, _('Festival')),
        (TOURNEUR, _('Tourneur')),
        (PRODUCTEUR, _('Producteur')),
        (META, _('Agenda culturel')),
        (ROOT, _('Tenant public root')),
    ]

    categorie = models.CharField(max_length=3, choices=CATEGORIE_CHOICES, default=SALLE_SPECTACLE,
                                         verbose_name=_("Categorie"))

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return f"{self.name} {self.get_categorie_display()}"

class Domain(DomainMixin):
    pass