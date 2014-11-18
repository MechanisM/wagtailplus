"""
Contains model class definitions.
"""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy  as _

from taggit.managers import TaggableManager
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailadmin.edit_handlers import FieldRowPanel
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel
from wagtail.wagtailadmin.edit_handlers import ObjectList
from wagtail.wagtailadmin.taggable import TagSearchable
from wagtail.wagtailsearch import index


@python_2_unicode_compatible
class Link(models.Model, TagSearchable):
    """
    Stores either a URL or an email address.
    """
    LINK_TYPE_EXTERNAL  = 1
    LINK_TYPE_EMAIL     = 2

    created_at      = models.DateTimeField(auto_now_add=True)
    link_type       = models.PositiveIntegerField(_(u'Link Type'), editable=False)
    title           = models.CharField(_(u'Title'), max_length=100, help_text=_(u'Enter a title for this link'))
    external_url    = models.URLField(_(u'URL'), null=True, blank=True, help_text=_(u'Enter a valid URL, including scheme (e.g. http://)'))
    email           = models.EmailField(_(u'Email'), null=True, blank=True, help_text=_(u'Enter a valid email address'))
    tags            = TaggableManager(help_text=None, blank=True, verbose_name=_(u'Tags'))

    class Meta(object):
        verbose_name        = _(u'Link')
        verbose_name_plural = _(u'Links')
        ordering            = ('title',)

    # Make address searchable.
    search_fields = [
        index.SearchField('title', partial_match=True, boost=10),
        index.SearchField('get_tags', partial_match=True, boost=10),
        index.SearchField('external_url'),
        index.SearchField('email'),
    ]

    def __str__(self):
        """
        Returns link title.

        :rtype: str.
        """
        return '{0}'.format(self.title)

    def get_absolute_url(self):
        """
        Returns link URL.

        :rtype: str.
        """
        url = self.external_url
        if self.email:
            url = 'mailto:{}'.format(self.email)
        return url

    @property
    def url(self):
        """
        Returns link URL.

        :rtype: str.
        """
        return self.get_absolute_url()

    def clean_fields(self, exclude=None):
        """
        Cleans model instance fields.

        :raises django.core.exceptions.ValidationError: if validation fails.
        """
        errors = {}

        # Make sure we have either an external URL or an email address,
        # but not both.
        if self.email and self.external_url:
            msg = _(u'A link cannot contain both an email address and a URL.')
            for field_name in ['external_url', 'email']:
                errors[field_name] = msg
        if not self.email and not self.external_url:
            msg = _(u'A link must contain either an email address or a URL.')
            for field_name in ['external_url', 'email']:
                errors[field_name] = msg

        # Make sure each link is unique.
        manager = self.__class__.objects.exclude(pk=self.pk)
        err_msg = _(u'A link already exists for this {0}.')
        if self.external_url:
            if manager.filter(external_url=self.external_url).count() > 0:
                errors['external_url'] = err_msg.format('URL')
        if self.email:
            if manager.filter(email=self.email).count() > 0:
                errors['email'] = err_msg.format('email address')

        # Raise any validation errors.
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """
        Saves the model instance.
        """
        # Set the link type.
        if self.external_url and not self.email:
            self.link_type = self.LINK_TYPE_EXTERNAL
        elif self.email and not self.external_url:
            self.link_type = self.LINK_TYPE_EMAIL

        super(Link, self).save(*args, **kwargs)

    @classmethod
    def get_edit_handler(cls):
        """
        Returns edit handler instance.

        :rtype: wagtail.wagtailadmin.edit_handlers.ObjectList.
        """
        return ObjectList(cls.content_panels)

Link.content_panels = [
    FieldPanel('title', classname='full title'),
    MultiFieldPanel([
        FieldRowPanel([
            FieldPanel('external_url', classname='col6'),
            FieldPanel('email', classname='col6'),
        ], classname='label-above'),
    ], _(u'Link Type (complete one or the other)')),
    FieldPanel('tags'),
]
