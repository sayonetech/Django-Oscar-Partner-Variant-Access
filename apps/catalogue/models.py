from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProduct
from django.utils.translation import ugettext_lazy as _


class Product(AbstractProduct):
    partner = models.ForeignKey('partner.Partner', verbose_name=_("Partner"),related_name='productPartner', null=True,blank=True)




from oscar.apps.catalogue.models import *  # noqa