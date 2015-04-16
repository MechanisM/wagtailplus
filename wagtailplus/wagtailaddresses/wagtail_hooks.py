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
        url(r'^addresses/', include(admin_urls)),
    ]

@hooks.register('register_admin_menu_item')
def register_locations_menu_item():
  return MenuItem('Addresses', reverse('wagtailaddresses_index'), classnames='icon icon-location', order=430)
