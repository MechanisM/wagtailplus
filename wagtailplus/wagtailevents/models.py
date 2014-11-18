"""
Contains model class definitions.
"""
import calendar
from collections import OrderedDict
from datetime import timedelta
from itertools import chain
from operator import attrgetter

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from modelcluster.fields import ParentalKey
from taggit.managers import TaggableManager
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailadmin.edit_handlers import FieldRowPanel
from wagtail.wagtailadmin.edit_handlers import InlinePanel
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel
from wagtail.wagtailadmin.edit_handlers import ObjectList
from wagtail.wagtailadmin.taggable import TagSearchable
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet

from natural.number import ordinal


NTH_WEEKDAYS = (
    (0, _(u'1st')),
    (1, _(u'2nd')),
    (2, _(u'3rd')),
    (3, _(u'4th')),
)

DAYS_OF_WEEK = (
    (0, _(u'Sunday')),
    (1, _(u'Monday')),
    (2, _(u'Tuesday')),
    (3, _(u'Wednesday')),
    (4, _(u'Thursday')),
    (5, _(u'Friday')),
    (6, _(u'Saturday')),
)

DAYS_OF_MONTH = ((x, x) for x in range(1, 32))

class EventManager(models.Manager):
    """
    Default manager for event model.
    """
    def date_range_generator(self, start_date, end_date):
        """
        Returns a generator for each date in specified range.

        :param start_date: the first date in range.
        :param end_date: the last date in range.
        :rtype: generator.
        """
        for d in range(int((end_date - start_date).days) + 1):
            yield start_date + timedelta(d)

    def is_nth_weekday(self, the_date, frequency):
        """
        Returns true if date is nth weekday according to frequency.

        :param the_date: the date instance to check.
        :param frequency: the EventFrequency instance to check against.
        :rtype: bool.
        """
        year        = int(the_date.strftime('%Y'))
        month       = int(the_date.strftime('%m'))
        date_dom    = int(the_date.strftime('%d'))
        bom, days   = calendar.monthrange(year, month)
        first       = (frequency.day_of_week - bom) % 7

        if xrange(first, days + 1, 7)[frequency.nth_weekday] == date_dom:
            return True
        return False

    def valid_date_generator(self, event, start_date, end_date):
        """
        Returns a generator of valid dates for specified event.

        :param event: the event instance.
        :param start_date: the first date in range.
        :param end_date: the last date in range.
        :rtype: generator.
        """
        # Iterate over each date in range.
        for the_date in self.date_range_generator(start_date, end_date):
            # Set individual date values.
            today       = timezone.now().date()
            date_dow    = int(the_date.strftime('%w'))
            date_dom    = int(the_date.strftime('%d'))
            # If there are no defined frequncies, return the first valid
            # date greater than or equal to today.
            if event.frequencies.count() == 0:
                if (the_date >= event.start_date) and (the_date >= today):
                    yield the_date
            # Iterate over each event frequency.
            for freq in event.frequencies.all():
                # First, check for a specified day of the week.
                if freq.day_of_week and freq.day_of_week == date_dow:
                    # Restrict to nth weekday of month?
                    if freq.nth_weekday:
                        if self.is_nth_weekday(the_date, freq):
                            yield the_date
                    # No restriction, OK to yield date.
                    else:
                        yield the_date
                # Next, check for day of month.
                if freq.day_of_month and freq.day_of_month == date_dom:
                    yield the_date
                # Finally, check for day period.
                if freq.day_period:
                    start_date = event.start_date
                    if ((the_date - start_date).days % freq.day_period == 0):
                        yield the_date

    def get_events(self, start, end):
        """
        Returns a dictionary of event instances keyed by date that occur
        within the specified date range (e.g., a calendar month).

        :param start: the first date in range.
        :param end: the last date in range.
        :rtype: dict.
        """
        events  = {}
        filters = {'start_date__lte': end, 'end_date__gte': start}

        # Iterate over events then check for valid dates within range.
        for event in self.filter(**filters):
            for valid_date in self.valid_date_generator(event, start, end):
                if valid_date not in events:
                    events[valid_date] = [event]
                else:
                    events[valid_date].append(event)

        # Return dictionary sorted by date.
        return OrderedDict(sorted(events.items(), key=lambda x: x[0]))

    def get_next_occurrence(self, event):
        """
        Returns next scheduled date for specified event.

        :param event: the event instance.
        :rtype: datetime.date.
        """
        # If the event's start and end dates are the same, return it.
        if event.start_date == event.end_date:
            return event.start_date

        # Use valid date generator to find the next valid event date.
        start       = timezone.now().date()
        generator   = self.valid_date_generator(event, start, event.end_date)

        return next(generator, None)

@python_2_unicode_compatible
class EventFrequency(models.Model):
    """
    Stores a date-based pattern for repeating events.
    """
    event           = ParentalKey('wagtailevents.Event', related_name='frequencies')
    day_of_week     = models.PositiveIntegerField(_(u'Weekday'), choices=DAYS_OF_WEEK, blank=True, null=True, help_text=_(u'Event will recur every specified day of the week'))
    nth_weekday     = models.PositiveIntegerField(_(u'Every Nth Weekday of the Month'), choices=NTH_WEEKDAYS, blank=True, null=True, help_text=_(u'Event will recur every nth specified day of the week'))
    day_of_month    = models.PositiveIntegerField(_(u'Day of Month'), choices=DAYS_OF_MONTH, blank=True, null=True, help_text=_(u'Event will recur every nth day of each month'))
    day_period      = models.PositiveIntegerField(_(u'Day Period'), blank=True, null=True, help_text=_(u'Event will recur every n number of days'))

    panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('day_period', classname='col6'),
                FieldPanel('day_of_month', classname='col6'),
            ], classname='label-above'),
            FieldRowPanel([
                FieldPanel('day_of_week', classname='col6'),
                FieldPanel('nth_weekday', classname='col6')
            ], classname='label-above'),
        ]),
    ]

    class Meta(object):
        verbose_name        = _(u'Event Frequency')
        verbose_name_plural = _(u'Event Frequencies')

    def __str__(self):
        """
        Returns frequency description.

        :rtype: str.
        """
        label = 'Every Day'
        if self.day_of_week:
            day_name    = unicode(DAYS_OF_WEEK[self.day_of_week][1])
            label       = 'Every {0}'.format(day_name)
            if self.nth_weekday:
                nth_day = unicode(NTH_WEEKDAYS[self.nth_weekday][1])
                label   = 'Every {0} {1}'.format(nth_day, day_name)

        elif self.day_of_month:
            label = 'Every {0} of the Month'.format(ordinal(self.day_of_month))

        elif self.day_period:
            label = 'Every {0} Days'.format(self.day_period)

        return label

    def clean_fields(self, exclude=None):
        """
        Cleans model instance fields.

        :param exclude: list of fields to exclude.
        """
        errors = {}

        # Make sure we have a weekday if we're specifying an nth weekday.
        if self.nth_weekday and not self.day_of_week:
            label   = NTH_WEEKDAYS[self.nth_weekday][1]
            msg     = _(u'Which {0} day of the month does this event recur on?')
            errors['day_of_week'] = msg.format(label)

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """
        Saves the model instance.
        """
        # Clean up values if multiple conflicting selections were made.
        if self.day_of_week:
            self.day_of_month   = None
            self.day_period     = None
        elif self.day_of_month:
            self.day_period = None

        super(EventFrequency, self).save(*args, **kwargs)

@python_2_unicode_compatible
class Event(models.Model, TagSearchable):
    """
    Stores an event that has the ability to repeat at specified frequencies.
    """
    created_at  = models.DateTimeField(_(u'Created'), auto_now_add=True)
    name        = models.CharField(_(u'Name'), max_length=100, unique=True)
    start_date  = models.DateField(_(u'Start Date'), db_index=True, help_text=_(u'Enter the first date of a repeating event, or the date of a one-time event.'))
    end_date    = models.DateField(_(u'End Date'), db_index=True, help_text=_(u'Enter the last date of a repeating event, or the date of a one-time event.'))
    tags        = TaggableManager(help_text=None, blank=True, verbose_name=_('Tags'))
    objects     = EventManager()

    # Make event searchable.
    search_fields = [
        index.SearchField('name', partial_match=True, boost=10),
        index.SearchField('get_tags', partial_match=True, boost=10),
        index.SearchField('get_frequencies')
    ]

    class Meta(object):
        verbose_name        = _(u'Event')
        verbose_name_plural = _(u'Events')
        ordering            = ('name',)

    @property
    def frequency(self):
        """
        Returns event frequencies as a comma-separated string.

        :rtype: str.
        """
        if self.frequencies.count() > 0:
            return ', '.join([str(f) for f in self.frequencies.all()])
        return 'Every Day'

    @property
    def next_occurrence(self):
        """
        Returns next event occurrence, if one is scheduled.

        :rtype: datetime.date.
        """
        return Event.objects.get_next_occurrence(self)

    def __str__(self):
        """
        Returns event name.

        :rtype: str.
        """
        return '{0}'.format(self.name)

    def clean_fields(self, exclude=None):
        """
        Cleans model instance fields.
        """
        errors = {}

        # Make sure dates are sane.
        if self.end_date < self.start_date:
            msg = _(u'End date must be greater than or equal to start date.')
            errors['end_date'] = msg

        if errors:
            raise ValidationError(errors)

    def get_pages(self, date):
        """
        Returns list of event pages for specified date.

        :param date: the event date.
        :rtype: list.
        """
        querysets = []

        # Iterate over models, looking for any that subclass BaseEventPage.
        for model in models.get_models():
            if issubclass(model, BaseEventPage):
                # First, look for pages matching the specified date.
                queryset = model.objects.filter(event=self, date=date)
                if queryset.count() > 0:
                    querysets.append(queryset)
                # If no matches are found, look for a "default" page.
                else:
                    querysets.append(
                        model.objects.filter(event=self, date__isnull=True)
                    )

        # Return a single list, sorted by start time.
        return sorted(chain(*querysets), key=attrgetter('start'))

    @classmethod
    def get_edit_handler(cls):
        """
        Returns edit handler instance.

        :rtype: wagtail.wagtailadmin.edit_handlers.ObjectList.
        """
        return ObjectList(cls.content_panels)

Event.content_panels = [
    FieldPanel('name', classname='full title'),
    MultiFieldPanel([
        FieldRowPanel([
            FieldPanel('start_date', classname='col6'),
            FieldPanel('end_date', classname='col6'),
        ], classname='label-above'),
    ], _(u'Date Range'), classname='publishing'),
    InlinePanel(Event, 'frequencies', label=_(u'Frequencies')),
    FieldPanel('tags'),
]

class BaseEventPage(models.Model):
    """
    Abstract event page definition.
    """
    event   = models.ForeignKey('wagtailevents.Event', blank=True, null=True, verbose_name=_(u'Master Event'), related_name='pages', help_text=_(u'Leave blank if this is a one-time event and the master event will be created automatically.'))
    date    = models.DateField(_(u'Date'), db_index=True, blank=True, null=True, help_text=_(u'Leave blank if this is the default page for this event.'))
    start   = models.TimeField(_(u'Start Time'), blank=True, null=True, db_index=True)
    end     = models.TimeField(_(u'End Time'), blank=True, null=True)

    class Meta(object):
        abstract            = True
        verbose_name        = _(u'Event Page')
        verbose_name_plural = _(u'Event Pages')
        ordering            = ('start',)
        unique_together     = ('event', 'date', 'start')

    @property
    def time_range(self):
        """
        Returns event time range.

        :rtype: str.
        """
        pattern = '%I:%M %p'
        result  = 'All Day'
        if self.start:
            result = self.start.strftime(pattern)
            if self.end:
                result = '{0} - {1}'.format(result, self.end.strftime(pattern))
        return result

    def clean(self):
        """
        Cleans instance.
        """
        # Make sure times are sane.
        if (self.end and self.start) and (self.end <= self.start):
            msg = _(u'End time must be greater than start time.')
            raise ValidationError(msg)

        # If we don't have a master event, create one.
        if not self.event:
            self.event, created = Event.objects.get_or_create(
                name=self.title,
                start_date=self.date,
                end_date=self.date
            )

    def get_date(self):
        """
        Returns event date - if page does not include a date value
        (i.e., it's being used as a default event page), then return
        the next scheduled event date.

        :rtype: datetime.date.
        """
        date = self.date
        if date is None:
            date = Event.objects.get_next_occurence(self.event)
        return date

BaseEventPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('event'),
    MultiFieldPanel([
        FieldRowPanel([
            FieldPanel('date', classname='col12'),
            FieldPanel('start', classname='col6'),
            FieldPanel('end', classname='col6'),
        ], classname='label-above'),
    ], 'Event Details', classname='publishing'),
]
