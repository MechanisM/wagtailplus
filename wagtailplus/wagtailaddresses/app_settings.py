"""
Contains app-specific settings.
"""
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


# Set default attribute map.
DEFAULT_ADDRESS_ATTR_MAP = {
    'street_number':                _(u'Street Number'),
    'route':                        _(u'Street Name'),
    'locality':                     _(u'City'),
    'administrative_area_level_2':  _(u'County'),
    'administrative_area_level_1':  _(u'State'),
    'postal_code':                  _(u'Postal Code'),
    'country':                      _(u'Country'),
}

# Set default address format.
DEFAULT_ADDRESS_FORMAT = '{0} {1}, {2}, {3} {4}'

# Set default address format fields.
DEFAULT_ADDRESS_FORMAT_FIELDS = [
    'street_number',
    'route',
    'locality',
    'administrative_area_level_1',
    'postal_code'
]

ADDRESS_ATTR_MAP        = getattr(settings, 'ADDRESS_ATTR_MAP', DEFAULT_ADDRESS_ATTR_MAP)
ADDRESS_FORMAT          = getattr(settings, 'ADDRESS_FORMAT', DEFAULT_ADDRESS_FORMAT)
ADDRESS_FORMAT_FIELDS   = getattr(settings, 'ADDRESS_FORMAT_FIELDS', DEFAULT_ADDRESS_FORMAT_FIELDS)
