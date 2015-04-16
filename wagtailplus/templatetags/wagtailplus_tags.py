"""
Contains wagtail plus tags.
"""
from django import template
from django.utils.safestring import mark_safe

from wagtailplus.rich_text import expand_db_html



register = template.Library()

@register.filter
def flexiblerichtext(value):
    """
    Returns HTML from specified value.

    :param value: the value to return.
    :rtype: str.
    """
    if value is not None:
        html = expand_db_html(value)
    else:
        html = ''

    return mark_safe(html)
