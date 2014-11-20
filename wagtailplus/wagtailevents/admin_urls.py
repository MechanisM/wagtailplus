"""
Contains admin URLs.
"""
from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from wagtailplus.views import chooser
from wagtailplus.views import crud

from .models import Event


urlpatterns = [
    url(
        r'^$',
        permission_required('wagtailadmin.access_admin')(crud.IndexView.as_view(
            model=Event,
            index_template='wagtailevents/events/index.html',
            results_template='wagtailevents/events/results.html'
        )),
        name='wagtailevents_index'
    ),
    url(
        r'^add/$',
        permission_required('wagtailevents.add_event')(crud.CreateView.as_view(
            model=Event,
            template_name='wagtailevents/events/add.html',
            success_url='wagtailevents_index'
        )),
        name='wagtailevents_add_event'
    ),
    url(
        r'^edit/(?P<pk>\d+)/$',
        permission_required('wagtailadmin.change_event')(crud.UpdateView.as_view(
            model=Event,
            template_name='wagtailevents/events/edit.html',
            success_url='wagtailevents_index'
        )),
        name='wagtailevents_edit_event'
    ),
    url(
        r'^delete/(?P<pk>\d+)/$',
        permission_required('wagtailadmin.delete_event')(crud.DeleteView.as_view(
            model=Event,
            template_name='wagtailevents/events/confirm_delete.html',
            success_url='wagtailevents_index'
        )),
        name='wagtailevents_delete_event'
    ),
    # Event chooser URLs.
    url(
        r'^chooser/$',
        chooser.ChooseView.as_view(
            model=Event,
            chooser_template='wagtailevents/chooser/chooser.html',
            results_template='wagtailevents/chooser/results.html',
            chooser_javascript='wagtailevents/chooser/chooser.js'
        ),
        name='wagtailevents_event_chooser'
    ),
    url(
        r'^chooser/create/$',
        chooser.CreateView.as_view(
            model=Event,
            chooser_template='wagtailevents/chooser/chooser.html',
            chooser_javascript='wagtailevents/chooser/chooser.js',
            chosen_javascript='wagtailevents/chooser/chosen.js'
        ),
        name='wagtailevents_event_chooser_create'
    ),
    url(
        r'^chooser/(?P<pk>\d+)/$',
        chooser.ChosenView.as_view(
            model=Event,
            chosen_javascript='wagtailevents/chooser/chosen.js'
        ),
        name='wagtailevents_event_chosen'
    ),
]
