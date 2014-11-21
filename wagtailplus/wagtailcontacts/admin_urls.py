"""
Contains admin URLs.
"""
from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from wagtailplus.views import chooser
from wagtailplus.views import crud

from .forms import ContactForm
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
    # Contact chooser URLs.
    url(
        r'^chooser/$',
        chooser.ChooseView.as_view(
            model=Contact,
            chooser_template='wagtailcontacts/chooser/chooser.html',
            results_template='wagtailcontacts/chooser/results.html',
            chooser_javascript='wagtailcontacts/chooser/chooser.js',
            form_class=ContactForm
        ),
        name='wagtailcontacts_contact_chooser'
    ),
    url(
        r'^chooser/create/$',
        chooser.CreateView.as_view(
            model=Contact,
            chooser_template='wagtailcontacts/chooser/chooser.html',
            chooser_javascript='wagtailcontacts/chooser/chooser.js',
            chosen_javascript='wagtailcontacts/chooser/chosen.js',
            form_class=ContactForm
        ),
        name='wagtailcontacts_contact_chooser_create'
    ),
    url(
        r'^chooser/(?P<pk>\d+)/$',
        chooser.ChosenView.as_view(
            model=Contact,
            chosen_javascript='wagtailcontacts/chooser/chosen.js'
        ),
        name='wagtailcontacts_contact_chosen'
    ),
]