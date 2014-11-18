"""
Contains admin URLs.
"""
from django.conf.urls import url

from wagtailplus.wagtaillinks.views import choosers


urlpatterns = [
    url(
        r'^choose-external-link/$',
        choosers.ExternalLinkChooseView.as_view(),
        name='wagtailadmin_choose_page_external_link'
    ),
    url(
        r'^choose-email-link/$',
        choosers.EmailLinkChooseView.as_view(),
        name='wagtailadmin_choose_page_email_link'
    ),
]