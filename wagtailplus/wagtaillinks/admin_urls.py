"""
Contains admin URLs.
"""
from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from wagtailplus.views import chooser
from wagtailplus.views import crud

from .models import Link
from .views import choosers


urlpatterns = [
    url(
        r'^$',
        permission_required('wagtailadmin.access_admin')(crud.IndexView.as_view(
            model=Link,
            index_template='wagtaillinks/links/index.html',
            results_template='wagtaillinks/links/results.html'
        )),
        name='wagtaillinks_index'
    ),
    url(
        r'^add/$',
        permission_required('wagtaillinks.add_link')(crud.CreateView.as_view(
            model=Link,
            template_name='wagtaillinks/links/add.html',
            success_url='wagtaillinks_index'
        )),
        name='wagtaillinks_add_link'
    ),
    url(
        r'^edit/(?P<pk>\d+)/$',
        permission_required('wagtaillinks.change_link')(crud.UpdateView.as_view(
            model=Link,
            template_name='wagtaillinks/links/edit.html',
            success_url='wagtaillinks_index'
        )),
        name='wagtaillinks_edit_link'
    ),
    url(
        r'^delete/(?P<pk>\d+)/$',
        permission_required('wagtaillinks.delete_link')(crud.DeleteView.as_view(
            model=Link,
            template_name='wagtaillinks/links/confirm_delete.html',
            success_url='wagtaillinks_index'
        )),
        name='wagtaillinks_delete_link'
    ),
    # Link chooser URLs.
    url(
        r'^chooser/$',
        choosers.LinkChooseView.as_view(),
        name='wagtaillinks_link_chooser'
    ),
    url(
        r'^chooser/create/$',
        choosers.LinkCreateView.as_view(),
        name='wagtaillinks_link_chooser_create'
    ),
    url(
        r'^chooser/(?P<pk>\d+)/$',
        choosers.LinkChosenView.as_view(),
        name='wagtaillinks_link_chosen'
    ),
    # URLs to allow for the creation and embedding of new links.
    url(
        r'^chooser/create-and-embed-external-link/$',
        choosers.CreateAndEmbedLinkView.as_view(
            chooser_template='wagtaillinks/chooser/external-chooser.html',
            chooser_javascript='wagtaillinks/chooser/chooser.js'
        ),
        name='wagtaillinks_link_chooser_create_and_embed_external'
    ),
    url(
        r'^chooser/create-and-embed-email-link/$',
        choosers.CreateAndEmbedLinkView.as_view(
            chooser_template='wagtaillinks/chooser/email-chooser.html',
            chooser_javascript='wagtaillinks/chooser/chooser.js'
        ),
        name='wagtaillinks_link_chooser_create_and_embed_email'
    ),
]