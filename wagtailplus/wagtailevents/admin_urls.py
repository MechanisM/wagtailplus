"""
Contains admin URLs.
"""
from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

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
        permission_required('wagtailadmin.access_admin')(crud.UpdateView.as_view(
            model=Event,
            template_name='wagtailevents/events/edit.html',
            success_url='wagtailevents_index'
        )),
        name='wagtailevents_edit_event'
    ),
    url(
        r'^delete/(?P<pk>\d+)/$',
        permission_required('wagtailadmin.access_admin')(crud.DeleteView.as_view(
            model=Event,
            template_name='wagtailevents/events/confirm_delete.html',
            success_url='wagtailevents_index'
        )),
        name='wagtailevents_delete_event'
    ),
]
