"""
Contains form field related classes.
"""
from django.db import models
from django.forms import Textarea

from wagtail.wagtailadmin.edit_handlers import BaseRichTextFieldPanel

from .rich_text import FlexibleDbWhitelister
from .rich_text import expand_db_html


def FlexibleRichTextFieldPanel(field_name, classname=''):
    """
    Field panel for flexible rich-text area.
    """
    return type(str('_FlexibleRichTextFieldPanel'), (BaseRichTextFieldPanel,), {
        'field_name':   field_name,
        'classname':    classname,
    })

class FlexibleRichTextArea(Textarea):
    """
    Prevents automatic replacement of 'DIV' tags with 'P' tags.
    """
    def get_panel(self):
        """
        Returns panel class for flexible rich text area.
        """
        return FlexibleRichTextFieldPanel

    def render(self, name, value, attrs=None):
        """
        Returns rendered content for flexible rich text area.

        :param name: element name.
        :param value: element value.
        :param attrs: element attributes.
        :rtype: str.
        """
        if value is None:
            translated_value = None
        else:
            translated_value = expand_db_html(value, for_editor=True)

        return super(FlexibleRichTextArea, self).render(
            name,
            translated_value,
            attrs
        )

    def value_from_datadict(self, data, files, name):
        """
        Returns cleaned value.

        :param data: data dictionary.
        :param files: files dictionary.
        :param name: widget name.
        :rtype: str.
        """
        original_value = super(FlexibleRichTextArea, self).value_from_datadict(
            data,
            files,
            name
        )

        if original_value is None:
            return None

        return FlexibleDbWhitelister.clean(original_value)

class FlexibleRichTextField(models.TextField):
    """
    Prevents automatic replacement of 'DIV' tags with 'P' tags.
    """
    def formfield(self, **kwargs):
        """
        Uses FlexibleRichTextArea as default widget.
        """
        defaults = {'widget': FlexibleRichTextArea}

        defaults.update(kwargs)

        return super(FlexibleRichTextField, self).formfield(**defaults)
