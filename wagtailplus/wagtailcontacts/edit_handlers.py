"""
Contains chooser panels for model instances.
"""
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from wagtail.wagtailadmin.edit_handlers import BaseChooserPanel


class BaseContactChooserPanel(BaseChooserPanel):
    """
    Address component chooser panel class.
    """
    field_template      = 'wagtailcontacts/edit_handlers/contact_chooser_panel.html'
    object_type_name    = 'contact'
    js_function_name    = 'createContactChooser'

def ContactChooserPanel(field_name):
    """
    Returns choser panel class with specified field name.

    :param field_name: field name of chosen model.
    """
    return type('_ContactChooserPanel', (BaseContactChooserPanel,), {
        'field_name': field_name,
    })
