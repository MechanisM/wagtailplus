"""
Contains model class definitions.
"""
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailcore.templatetags.rich_text import richtext


__ALL__ = [
    'BasePageBlock',
    'BaseMultiBlockPage',
]

@python_2_unicode_compatible
class BasePageBlock(Orderable, Publishable):
    """
    Abstract page block definition.
    """
    css     = models.CharField(_(u'CSS Class'), max_length=100, blank=True, help_text=_(u'Enter an optional CSS class string for this block'))
    content = RichTextField(_(u'Content'), blank=True, help_text=_(u'Enter the content for this block'))

    panels  = [
        FieldPanel('css'),
        FieldPanel('content'),
    ]

    class Meta(object):
        ordering = ('sort_order',)

    def __str__(self):
        """
        Returns block label.

        :rtype: str.
        """
        return 'Block #{0}'.format(self.sort_order + 1)

    def render(self):
        """
        Returns rendered block content.

        :rtype: unicode.
        """
        html    = richtext(self.content)
        css     = 'block block-{0}'.format(self.pk)
        if self.css:
            css = '{0} {1}'.format(css, self.css)
        return u'<div class="{0}">{1}</div>'.format(css, html)

class BaseMultiBlockPage(object):
    """
    Abstract multi-block page definition.
    """
    @property
    def plain_content(self):
        """
        Returns page content without HTML tags.

        :rtype: unicode.
        """
        return u'{0}'.format(strip_tags(self.content))

    @property
    def content(self):
        """
        Returns page content.

        :rtype: unicode.
        """
        content = []
        if hasattr(self, 'blocks'):
            for block in self.blocks.all():
                content.append(block.render())

        return u'\n'.join(content)
