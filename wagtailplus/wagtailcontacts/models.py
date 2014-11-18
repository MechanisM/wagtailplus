"""
Contains model class definitions.
"""
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from localflavor.us.models import PhoneNumberField
from taggit.managers import TaggableManager
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel
from wagtail.wagtailadmin.edit_handlers import ObjectList
from wagtail.wagtailadmin.taggable import TagSearchable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtailplus.wagtailaddresses.edit_handlers import AddressChooserPanel


class Contact(models.Model, TagSearchable):
    """
    Basic contact.
    """
    created_at  = models.DateTimeField(auto_now_add=True)
    name        = models.CharField(_(u'Name'), max_length=100, db_index=True, help_text=_(u'Enter a name for this contact'))
    website     = models.URLField(_(u'Website'), null=True, blank=True, help_text=_(u'Enter an optional website for this contact'))
    email       = models.EmailField(_(u'Email'), null=True, blank=True, help_text=_(u'Enter an optional email address for this contact'))
    telephone   = PhoneNumberField(_(u'Telephone'), null=True, blank=True, help_text=_(u'Enter an optional telephone number for this contact'))
    address     = models.ForeignKey('wagtailaddresses.Address', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text=_(u'Select an optional address for this contact'))
    image       = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text=_(u'Select an optional image for this contact'))
    tags        = TaggableManager(verbose_name=_(u'Tags'), blank=True, help_text=None)

    class Meta(object):
        verbose_name        = _(u'Contact')
        verbose_name_plural = _(u'Contacts')
        ordering            = ('name',)
        unique_together     = (('name', 'website'), ('name', 'email'))

    # Make address searchable.
    search_fields = [
        index.SearchField('name', partial_match=True, boost=10),
        index.SearchField('get_tags', partial_match=True, boost=10),
        index.SearchField('website'),
        index.SearchField('email'),
        index.SearchField('telephone'),
    ]

    def __str__(self):
        """
        Returns contact name.

        :rtype: str.
        """
        return '{0}'.format(self.name)

    @classmethod
    def get_edit_handler(cls):
        """
        Returns edit handler instance.

        :rtype: wagtail.wagtailadmin.edit_handlers.ObjectList.
        """
        return ObjectList(cls.content_panels)

Contact.content_panels = [
    FieldPanel('name', classname='full title'),
    MultiFieldPanel([
        FieldPanel('website'),
        FieldPanel('email'),
        FieldPanel('telephone'),
        AddressChooserPanel('address'),
    ], _(u'General Information')),
    ImageChooserPanel('image'),
    FieldPanel('tags'),
]
