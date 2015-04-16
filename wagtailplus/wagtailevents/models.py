"""
Contains model class definitions.
"""
from datetime import datetime
from datetime import time

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from schedule.models import Event
from taggit.managers import TaggableManager
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailadmin.edit_handlers import FieldRowPanel
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel
from wagtail.wagtailadmin.taggable import TagSearchable
from wagtail.wagtailcore.models import PageManager

from .edit_handlers import EventChooserPanel


class BaseEvent(Event, TagSearchable):
    """
    Adds tags to schedule.Event.
    """
    tags = TaggableManager(blank=True)

    panels = [
        FieldPanel('title', classname='full title'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('start', classname='col6'),
                FieldPanel('end', classname='col6'),
            ], classname='label-above'),
        ], _(u'Date Range'), classname='publishing'),
        FieldPanel('description'),
        FieldPanel('rule'),
        FieldPanel('tags'),
    ]

    class Meta(object):
        app_label           = 'wagtailevents'
        verbose_name        = 'Event'
        verbose_name_plural = 'Events'
        ordering            = ('-start', 'title',)

def delete_event(sender, instance, **kwargs):
    """
    Deletes root event instance corresponding to base event instance.

    :param sender: the sending class.
    :param instance: the base event instance.
    """
    Event.objects.filter(pk=instance.event_ptr_id).delete()

# Connect receiver to signal so that root event instance is also deleted.
models.signals.post_delete.connect(
    delete_event,
    sender          = BaseEvent,
    dispatch_uid    = 'delete_event'
)

class EventPageManager(PageManager):
    """
    Custom manager class for event pages.
    """
    def get_queryset(self):
        """
        Returns queryset of upcoming events.

        :rtype: django.db.models.query.QuerySet.
        """
        qs      = super(EventPageManager, self).get_queryset()
        today   = timezone.now().date()
        start   = datetime.combine(today, time(0, 0))
        start   = timezone.make_aware(start, timezone.get_current_timezone())

        return qs.live().filter(start__gte=start)

class BaseEventPage(models.Model):
    """
    Abstract event page definition.
    """
    event       = models.ForeignKey('wagtailevents.BaseEvent', blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_(u'Master Event'), related_name='+', help_text=_(u'Leave blank if this is a one-time event and the master event will be created automatically.'))
    start       = models.DateTimeField(_(u'Event Start'), db_index=True)
    end         = models.DateTimeField(_(u'Event End'), blank=True, null=True)
    upcoming    = EventPageManager()

    class Meta(object):
        abstract    = True
        ordering    = ('-start',)

    @property
    def time_range(self):
        """
        Returns event time range.

        :rtype: str.
        """
        pattern = '%I:%M %p'
        result  = self.start.time().strftime(pattern)

        if self.end:
             result = '{0} - {1}'.format(
                result,
                self.end.time().strftime(pattern)
            )

        return result

    def clean(self):
        """
        Cleans instance.
        """
        # Make sure times are sane.
        if (self.end) and (self.end <= self.start):
            msg = _(u'Event end must be greater than event start.')
            raise ValidationError(msg)

        # If we don't have a master event, create one.
        if not self.event:
            self.event, created = BaseEvent.objects.get_or_create(
                title   = self.title,
                start   = self.start,
                end     = self.end or self.start
            )

BaseEventPage.content_panels = [
    FieldPanel('title', classname='full title'),
    EventChooserPanel('event'),
    MultiFieldPanel([
        FieldRowPanel([
            FieldPanel('start', classname='col6'),
            FieldPanel('end', classname='col6'),
        ], classname='label-above'),
    ], _(u'Event Details'), classname='publishing'),
]
