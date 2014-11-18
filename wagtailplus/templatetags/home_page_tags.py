"""
Contains template tags used in the admin home page.
"""
from django import template

from wagtailplus.wagtailaddresses.models import Address
from wagtailplus.wagtailcontacts.models import Contact
from wagtailplus.wagtailevents.models import Event
from wagtailplus.wagtaillinks.models import Link


register = template.Library()

@register.assignment_tag
def total_addresses():
    """
    Returns total number of address instances.

    :rtype: int.
    """
    return Address.objects.count()

@register.assignment_tag
def total_contacts():
    """
    Returns total number of link instances.

    :rtype: int.
    """
    return Contact.objects.count()

@register.assignment_tag
def total_events():
    """
    Returns total number of event instances.

    :rtype: int.
    """
    return Event.objects.count()

@register.assignment_tag
def total_links():
    """
    Returns total number of link instances.

    :rtype: int.
    """
    return Link.objects.count()
