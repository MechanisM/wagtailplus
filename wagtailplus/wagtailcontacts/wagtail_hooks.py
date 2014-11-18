from django.conf.urls import include
from django.conf.urls import url
from django.core.urlresolvers import reverse

from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks

from . import admin_urls

@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^contacts/', include(admin_urls)),
    ]

@hooks.register('register_admin_menu_item')
def register_locations_menu_item():
  return MenuItem('Contacts', reverse('wagtailcontacts_index'), classnames='icon icon-user', order=440)