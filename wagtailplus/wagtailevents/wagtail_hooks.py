"""
Contains Wagtail CMS integration hooks.
"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks

from . import admin_urls

@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^wagtail-events/', include(admin_urls)),
    ]

@hooks.register('register_admin_menu_item')
def register_locations_menu_item():
  return MenuItem('Events', reverse('wagtailevents_index'), classnames='icon icon-date', order=420)

@hooks.register('insert_editor_js')
def editor_js():
    return format_html(
        """
        <script>
            window.chooserUrls.eventChooser = '{0}';
        </script>
        <script src='{1}wagtailevents/js/event-chooser.js'></script>
        """,
        reverse('wagtailevents_event_chooser'),
        settings.STATIC_URL
    )
