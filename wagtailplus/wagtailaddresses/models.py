"""
Contains model class definitions.
"""
import json

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from django.conf import settings
from django.contrib.gis.geos import Point
from django.utils.encoding import python_2_unicode_compatible
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel
from wagtail.wagtailadmin.edit_handlers import ObjectList
from wagtail.wagtailadmin.taggable import TagSearchable
from wagtail.wagtailsearch import index

from .app_settings import ADDRESS_ATTR_MAP
from .app_settings import ADDRESS_FORMAT
from .app_settings import ADDRESS_FORMAT_FIELDS
from .edit_handlers import AddressComponentChooserPanel


API_KEY = getattr(settings, 'GOOGLE_API_KEY', None)

# Test for GIS app - probably a better way to do this...
if 'django.contrib.gis' in settings.INSTALLED_APPS:
    # Use GIS-enabled classes.
    from django.contrib.gis.db import models
    GEO_ENABLED = True
    geom_field  = models.PointField(_('Geometry'), srid=4326, blank=True, null=True, editable=False)
    addr_mgr    = models.GeoManager
else:
    # Fall back to standard classes.
    from django.db import models
    GEO_ENABLED = False
    geom_field  = models.CharField(_(u'Geometry'), max_length=50, blank=True, null=True, editable=False)
    addr_mgr    = models.Manager

def get_address_data(addr_str):
    """
    Returns address data dictionary for specified string.

    :rtype: dict.
    """
    if API_KEY:
        url = 'https://maps.googleapis.com/maps/api/geocode/json?{0}'.format(
            urlencode({
                'key':      API_KEY,
                'address':  addr_str,
                'sensor':   False
            })
        )
    
        try:
            response    = urlopen(url)
            data        = json.loads(response.read())
            return data['results'][0]
        except:
            return None

def get_geom_from_data(data):
    """
    Returns geometry value (point object or string) from data dictionary.

    :param data: the address data dictionary.
    :rtype: django.contrib.gis.geos.Point || str.
    """
    if GEO_ENABLED:
        # Set the address geometry with SRID = 4326.
        geom = Point(
            data['geometry']['location']['lng'],
            data['geometry']['location']['lat'],
            srid=4326
        )
    else:
        # Simply store the latitude and longitude.
        geom = '{0},{1}'.format(
            data['geometry']['location']['lat'],
            data['geometry']['location']['lng'],
        )

    return geom

class AddressManager(addr_mgr):
    """
    Custom address model manager.
    """
    def get_or_create_from_string(self, addr_str):
        """
        Returns address model for specified string value.

        :param addr_str: the address string.
        :rtype: tuple.
        """
        addr    = None
        comps   = {}
        data    = get_address_data(addr_str)

        if data:
            for comp in data['address_components']:
                type = comp['types'][0]
                if type in ADDRESS_ATTR_MAP:
                    comps[type] = AddressComponent.objects.get_or_create(
                        type        = ADDRESS_ATTR_MAP[type],
                        long_name   = comp['long_name'],
                        short_name  = comp['short_name']
                    )[0]

            # Add default geometry value and return the instance.
            defaults = {'geom': get_geom_from_data(data)}
            return Address.objects.get_or_create(
                defaults={'geom': get_geom_from_data(data)},
                **comps
            )

        return (None, False)

@python_2_unicode_compatible
class AddressComponent(models.Model, TagSearchable):
    """
    Stores an address component record.
    """
    type        = models.CharField(_(u'Component Type'), max_length=50, db_index=True)
    short_name  = models.CharField(_(u'Short Name'), max_length=255, db_index=True)
    long_name   = models.CharField(_(u'Long Name'), max_length=255, db_index=True)
    tags        = TaggableManager(help_text=None, blank=True, verbose_name=_('Tags'))

    # Make component searchable.
    search_fields = [
        index.SearchField('short_name'),
        index.SearchField('long_name'),
    ]

    class Meta(object):
        ordering        = ('long_name',)
        unique_together = (('type', 'short_name'), ('type', 'long_name'))

    def __str__(self):
        """
        Returns component long name.

        :rtype: str.
        """
        return '{0}'.format(self.long_name)

@python_2_unicode_compatible
class Address(models.Model, TagSearchable):
    """
    Stores a composite address record.
    """
    created_at                  = models.DateTimeField(_(u'Created'), auto_now_add=True)
    geom                        = geom_field
    label                       = models.CharField(_(u'Label'), max_length=200, unique=True, editable=False)
    street_number               = models.CharField(_(u'Street Number'), max_length=6, db_index=True)
    route                       = models.ForeignKey('wagtailaddresses.AddressComponent', verbose_name=ADDRESS_ATTR_MAP['route'], related_name='+')
    locality                    = models.ForeignKey('wagtailaddresses.AddressComponent', verbose_name=ADDRESS_ATTR_MAP['locality'], related_name='+')
    administrative_area_level_2 = models.ForeignKey('wagtailaddresses.AddressComponent', verbose_name=ADDRESS_ATTR_MAP['administrative_area_level_2'], related_name='+', blank=True, null=True)
    administrative_area_level_1 = models.ForeignKey('wagtailaddresses.AddressComponent', verbose_name=ADDRESS_ATTR_MAP['administrative_area_level_1'], related_name='+')
    postal_code                 = models.ForeignKey('wagtailaddresses.AddressComponent', verbose_name=ADDRESS_ATTR_MAP['postal_code'], related_name='+')
    country                     = models.ForeignKey('wagtailaddresses.AddressComponent', verbose_name=ADDRESS_ATTR_MAP['country'], related_name='+')
    tags                        = TaggableManager(help_text=None, blank=True, verbose_name=_('Tags'))
    objects                     = AddressManager()

    class Meta(object):
        verbose_name        = _(u'Address')
        verbose_name_plural = _(u'Addresses')
        unique_together     = ('street_number', 'route', 'postal_code')

    # Make address searchable.
    search_fields = [
        index.SearchField('label', partial_match=True, boost=10),
        index.SearchField('get_tags', partial_match=True, boost=10),
    ]

    @property
    def latitude(self):
        """
        Returns address latitude, if available.

        :rtype: float.
        """
        lat = None
        if self.geom:
            if GEO_ENABLED:
                lat = self.geom.y
            else:
                lat, lon = self.geom.split(',')
        return lat

    @property
    def longitude(self):
        """
        Returns address longitude, if available.

        :rtype: float.
        """
        lon = None
        if self.geom:
            if GEO_ENABLED:
                lon = self.geom.x
            else:
                lat, lon = self.geom.split(',')
        return lon

    def __str__(self):
        """
        Returns formatted address.

        :rtype: str.
        """
        format_values = []
        for field in ADDRESS_FORMAT_FIELDS:
            format_values.append(getattr(self, field, ''))
        return ADDRESS_FORMAT.format(*format_values)

    def save(self, *args, **kwargs):
        """
        Automatically sets address geometry and saves instance.
        """
        # Set address label.
        self.label = self.__str__()

        # Attempt to set geometry if empty.
        if not self.geom:
            data = get_address_data(self.__str__())
            if data:
                self.geom = get_geom_from_data(data)

        super(Address, self).save(*args, **kwargs)

    @classmethod
    def get_edit_handler(cls):
        """
        Returns edit handler instance.

        :rtype: wagtail.wagtailadmin.edit_handlers.ObjectList.
        """
        return ObjectList(cls.content_panels)

Address.content_panels = [
    FieldPanel('street_number', classname='full title'),
    MultiFieldPanel([
        AddressComponentChooserPanel('route'),
        AddressComponentChooserPanel('locality'),
        AddressComponentChooserPanel('administrative_area_level_2'),
        AddressComponentChooserPanel('administrative_area_level_1'),
        AddressComponentChooserPanel('postal_code'),
        AddressComponentChooserPanel('country'),
    ], _(u'Address Components')),
    FieldPanel('tags'),
]
