from django.conf.urls import include
from django.conf.urls import url
from django.core.urlresolvers import reverse

from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks

from . import admin_urls

@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^events/', include(admin_urls)),
    ]

@hooks.register('register_admin_menu_item')
def register_locations_menu_item():
  return MenuItem('Events', reverse('wagtailevents_index'), classnames='icon icon-date', order=420)