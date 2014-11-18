from django import forms

from .app_settings import ADDRESS_ATTR_MAP
from .models import Address
from .models import AddressComponent


class AddressForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta(object):
        model = Address

    def __init__(self, *args, **kwargs):
        """
        Initializes the form instance, restricted the queryset of each
        component field to those specific component types.
        """
        super(AddressForm, self).__init__(*args, **kwargs)

        for field, component in ADDRESS_ATTR_MAP.iteritems():
            queryset = AddressComponent.objects.all()
            if field in self.fields:
                self.fields[field].queryset = queryset.filter(type=component)

class AddressComponentForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta(object):
        model   = AddressComponent
        fields  = ('short_name', 'long_name')
