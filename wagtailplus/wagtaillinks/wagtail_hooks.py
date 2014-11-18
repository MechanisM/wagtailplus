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
        url(r'^links/', include(admin_urls)),
    ]

@hooks.register('register_admin_menu_item')
def register_locations_menu_item():
  return MenuItem('Links', reverse('wagtaillinks_index'), classnames='icon icon-link', order=410)

@hooks.register('insert_editor_js')
def editor_js():
    return format_html(
        """
        <script>
            window.chooserUrls.linkChooser = '{0}';
        </script>
        """,
        reverse('wagtaillinks_link_chooser')
    )
