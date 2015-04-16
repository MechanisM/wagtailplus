"""
Contains Wagtail CMS integration hooks.
"""
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from wagtail.wagtailcore import hooks


@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        """
        <link rel="stylesheet" href="{0}wagtailplus/scss/hallo.scss" type="text/x-scss" />
        """,
        settings.STATIC_URL
    )

@hooks.register('insert_editor_js')
def enable_source():
    return format_html(
        """
        <script src="{0}wagtailplus/js/hallo-plugins.js"></script>
        <script>
            window.toggleHalloSourceURL = '{1}';
            registerHalloPlugin('togglesource');
        </script>
        """,
        settings.STATIC_URL,
        reverse('toggle_hallo_source')
    )