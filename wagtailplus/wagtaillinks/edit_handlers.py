"""
Contains chooser panels for model instances.
"""
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from wagtail.wagtailadmin.edit_handlers import BaseChooserPanel


class BaseLinkChooserPanel(BaseChooserPanel):
    """
    Address component chooser panel class.
    """
    field_template      = 'wagtaillinks/edit_handlers/link_chooser_panel.html'
    object_type_name    = 'link'
    js_function_name    = 'createLinkChooser'

def LinkChooserPanel(field_name):
    """
    Returns choser panel class with specified field name.

    :param field_name: field name of chosen model.
    """
    return type('_LinkChooserPanel', (BaseLinkChooserPanel,), {
        'field_name': field_name,
    })
