"""
Contains event utility classes and functions.
"""
import calendar
from datetime import date
from datetime import datetime

from django.template.loader import render_to_string
from django.utils import timezone

from .models import Event


class EventCalendar(calendar.HTMLCalendar): # pylint: disable=R0904
    """
    Uses component templates to render HTML event calendar.
    """
    templates   = {
        'day-cell':     'wagtailevents/event-calendar/day-cell.html',
        'title-row':    'wagtailevents/event-calendar/title-row.html'
    }

    @classmethod
    def get_calendar(cls, year, month, templates=None):
        """
        Returns rendered HTML calendar.

        :param year: calendar year.
        :param month: calendar month.
        :param templates: dictionary of component templates.
        :rtype: str.
        """
        self        = cls()
        self.year   = int(year)
        self.month  = int(month)
        self.events = self.get_events()

        if templates:
            self.templates.update(templates)

        return self.formatmonth(self.year, self.month, True)

    def get_events_for_date(self, the_date):
        """
        Returns iterable of events for specified date.

        :param the_date: the event date.
        :rtype: iterable.
        """
        if the_date in self.events:
            return self.events[the_date]
        return []

    def formatday(self, day, weekday):
        """
        Returns an HTML table cell for specified day.

        :param day: the day of the month.
        :param weekday: the day of the week.
        :rtype: str.
        """
        context = {'css': self.cssclasses[weekday]}

        if day > 0:
            the_date    = date(self.year, self.month, day)
            events      = []

            for event in self.get_events_for_date(the_date):
                events.append({
                    'event':    event,
                    'pages':    event.get_pages(the_date)
                })
            
            context.update({'date': the_date, 'events': events})

        return render_to_string(self.templates['day-cell'], context)

    def formatmonthname(self, year, month, withyear=True):
        """
        Returns HTML table row with specified month name.

        :param withyear: whether or not to include the calendar year.
        :rtype: str.
        """
        context = {
            'month_name':   calendar.month_name[month],
            'year':         year if withyear else None,
            'prev':         self.get_previous(),
            'next':         self.get_next()
        }
        return render_to_string(self.templates['title-row'], context)

    def get_events(self):
        """
        Returns dictionary of events for calendar.

        :rtype: dict.
        """
        year    = self.year
        month   = self.month
        start   = date(year, month, 1)
        end     = date(year, month, calendar.monthrange(year, month)[1])

        return Event.objects.get_events(start, end)

    def get_next(self):
        """
        Returns tuple containing next month, year, and date (first of month).

        :rtype: tuple.
        """
        month   = 1 if self.month == 12 else self.month + 1
        year    = self.year + 1 if self.month == 12 else self.year
        return (month, year, datetime(year, month, 1))

    def get_previous(self):
        """
        Returns tuple containing previous month, year, and date (first of month).

        :rtype: tuple.
        """
        month   = 12 if self.month == 1 else self.month - 1
        year    = self.year - 1 if self.month == 1 else self.year
        return (month, year, datetime(year, month, 1))
