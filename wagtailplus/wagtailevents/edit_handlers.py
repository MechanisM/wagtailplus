"""
Contains chooser panels for model instances.
"""
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from wagtail.wagtailadmin.edit_handlers import BaseChooserPanel


class BaseEventChooserPanel(BaseChooserPanel):
    """
    Address component chooser panel class.
    """
    field_template      = 'wagtailevents/edit_handlers/event_chooser_panel.html'
    object_type_name    = 'event'
    js_function_name    = 'createEventChooser'

def EventChooserPanel(field_name):
    """
    Returns choser panel class with specified field name.

    :param field_name: field name of chosen model.
    """
    return type('_EventChooserPanel', (BaseEventChooserPanel,), {
        'field_name': field_name,
    })
