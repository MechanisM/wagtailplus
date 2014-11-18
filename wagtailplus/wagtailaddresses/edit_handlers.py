"""
Contains chooser panels for model instances.
"""
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from wagtail.wagtailadmin.edit_handlers import BaseChooserPanel


class BaseAddressComponentChooserPanel(BaseChooserPanel):
    """
    Address component chooser panel class.
    """
    field_template      = 'wagtailaddresses/edit_handlers/component_chooser_panel.html'
    object_type_name    = 'component'
    js_function_name    = 'createComponentChooser'

    def get_chooser_url(self, field_name):
        """
        Returns chooser URL for specified component.

        :param field_name: the component field name.
        :rtype: str.
        """
        url     = ''
        url_map = {
            'route':            reverse('wagtailaddresses_route_chooser'),
            'locality':         reverse('wagtailaddresses_locality_chooser'),
            'admin_level_2':    reverse('wagtailaddresses_admin_level_2_chooser'),
            'admin_level_1':    reverse('wagtailaddresses_admin_level_1_chooser'),
            'postal_code':      reverse('wagtailaddresses_postal_code_chooser'),
            'country':          reverse('wagtailaddresses_country_chooser'),
        }
        
        if field_name in url_map:
            url = url_map[field_name]
        return url

    def render_js(self):
        """
        Returns rendered JavaScript for edit handler.

        :rtype: str.
        """
        return mark_safe("{0}(fixPrefix('{1}'), '{2}');".format(
            self.js_function_name,
            self.bound_field.id_for_label,
            self.get_chooser_url(self.bound_field.name)
        ))

def AddressComponentChooserPanel(field_name):
    """
    Returns choser panel class with specified field name.

    :param field_name: field name of chosen model.
    """
    return type('_AddressComponentChooserPanel', (BaseAddressComponentChooserPanel,), {
        'field_name': field_name,
    })

class BaseAddressChooserPanel(BaseChooserPanel):
    """
    Address chooser panel class.
    """
    field_template      = 'wagtailaddresses/edit_handlers/address_chooser_panel.html'
    object_type_name    = 'address'
    js_function_name    = 'createAddressChooser'

def AddressChooserPanel(field_name):
    """
    Returns choser panel class with specified field name.

    :param field_name: field name of chosen model.
    """
    return type('_AddressChooserPanel', (BaseAddressChooserPanel,), {
        'field_name': field_name,
    })
