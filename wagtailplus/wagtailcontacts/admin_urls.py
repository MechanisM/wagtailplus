"""
Contains admin URLs.
"""
from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from wagtailplus.views import crud

from .models import Contact


urlpatterns = [
    url(
        r'^$',
        permission_required('wagtailadmin.access_admin')(crud.IndexView.as_view(
            model=Contact,
            index_template='wagtailcontacts/contacts/index.html',
            results_template='wagtailcontacts/contacts/results.html'
        )),
        name='wagtailcontacts_index'
    ),
    url(
        r'^add/$',
        permission_required('wagtailcontacts.add_contact')(crud.CreateView.as_view(
            model=Contact,
            template_name='wagtailcontacts/contacts/add.html',
            success_url='wagtailcontacts_index'
        )),
        name='wagtailcontacts_add_contact'
    ),
    url(
        r'^edit/(?P<pk>\d+)/$',
        permission_required('wagtailcontacts.change_contact')(crud.UpdateView.as_view(
            model=Contact,
            template_name='wagtailcontacts/contacts/edit.html',
            success_url='wagtailcontacts_index'
        )),
        name='wagtailcontacts_edit_contact'
    ),
    url(
        r'^delete/(?P<pk>\d+)/$',
        permission_required('wagtailcontacts.delete_contact')(crud.DeleteView.as_view(
            model=Contact,
            template_name='wagtailcontacts/contacts/confirm_delete.html',
            success_url='wagtailcontacts_index'
        )),
        name='wagtailcontacts_delete_contact'
    ),
]