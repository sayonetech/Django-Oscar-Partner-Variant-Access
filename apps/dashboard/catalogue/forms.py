from django import forms
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.forms.models import inlineformset_factory
from oscar.core.utils import slugify
from oscar.apps.catalogue.models import AttributeOption,AttributeOptionGroup
from oscar.core.loading import get_model
from oscar.forms.widgets import ImageInput
from oscar.apps.dashboard.catalogue.forms import ProductForm as CoreProductForm
from oscar.apps.dashboard.catalogue.forms import StockRecordForm as \
    CoreStockRecordForm
from oscar.apps.dashboard.catalogue.forms import StockRecordForm as CoreStockRecordForm
from oscar.apps.dashboard.catalogue.forms import StockRecordFormSet as CoreStockRecordFormSet

from oscar.apps.dashboard.catalogue.forms import ProductClassSelectForm as CoreProductClassSelectForm
from oscar.apps.dashboard.catalogue.forms import ProductSearchForm as CoreProductSearchForm


Product = get_model('catalogue', 'Product')
ProductClass = get_model('catalogue', 'ProductClass')
ProductAttribute = get_model('catalogue', 'ProductAttribute')
AttributeOptionGroup = get_model('catalogue', 'AttributeOptionGroup')
Partner = get_model('partner', 'Partner')
StockRecord = get_model('partner', 'StockRecord')
ProductImage = get_model('catalogue', 'ProductImage')



class ProductForm(CoreProductForm):
    partner = forms.ModelChoiceField(queryset=Partner.objects.all(), required=True)

    def __init__(self, user, *args, **kwargs):
        # The user kwarg is not used by stock StockRecordForm. We pass it
        # anyway in case one wishes to customise the partner queryset
        self.user = user
        super(ProductForm, self).__init__(*args, **kwargs)
        # Restrict accessible partners for non-staff users
        if self.instance.structure == "child":
            self.fields['partner'].initial = self.instance.parent.partner.id

        if not self.user.is_staff:
            self.fields['partner'].queryset = self.user.partners.all()
            self.fields['partner'].initial = Partner.objects.get(users=self.user)
            self.fields['partner'].widget = forms.HiddenInput()


    def save(self, commit=True):
        instance = super(ProductForm, self).save(commit=False)
        if self.instance.structure == "child":
            instance.title = self.instance.parent.title
            instance.partner = self.instance.parent.partner
            instance.description = self.instance.parent.description
        instance.save()
        if self.instance.structure == "parent":
            children = Product.objects.filter(structure="child", parent=instance)
            if children:
                for child in children:
                    child.title = self.instance.title
                    child.partner = self.instance.partner
                    child.description = self.instance.description
                    child.save()

        return instance



    class Meta(CoreProductForm.Meta):
        fields = ['partner','title', 'upc', 'description', 'is_discountable', 'structure']


class StockRecordForm(CoreStockRecordForm):

    def __init__(self, product_class, user, *args, **kwargs):
        # The user kwarg is not used by stock StockRecordForm. We pass it
        # anyway in case one wishes to customise the partner queryset
        self.user = user

        super(StockRecordForm, self).__init__(*args, **kwargs)
        # Restrict accessible partners for non-staff users
        if not self.user.is_staff:
            self.fields['partner'].queryset = self.user.partners.all()
            self.fields['partner'].initial = Partner.objects.get(users=self.user)
            self.fields['partner'].widget = forms.HiddenInput()

        # If not tracking stock, we hide the fields
        if not product_class.track_stock:
            for field_name in ['num_in_stock', 'low_stock_treshold']:
                if field_name in self.fields:
                    del self.fields[field_name]
        else:
            for field_name in ['price_excl_tax', 'num_in_stock']:
                if field_name in self.fields:
                    self.fields[field_name].required = True

class StockRecordFormSet(CoreStockRecordFormSet):

    def clean(self):
        pass