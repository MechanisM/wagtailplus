"""
Contains admin URLs.
"""
from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from .utils import get_component_urls
from .views import addresses
from .views import choosers


urlpatterns = [
    url(
        r'^$',
        permission_required('wagtailadmin.access_admin')(addresses.IndexView.as_view()),
        name='wagtailaddresses_index'
    ),
    url(
        r'^add/$',
        permission_required('wagtailaddresses.add_address')(addresses.CreateView.as_view()),
        name='wagtailaddresses_add_address'
    ),
    url(
        r'^edit/(?P<pk>\d+)/$',
        permission_required('wagtailaddresses.change_address')(addresses.UpdateView.as_view()),
        name='wagtailaddresses_edit_address'
    ),
    url(
        r'^delete/(?P<pk>\d+)/$',
        permission_required('wagtailaddresses.delete_address')(addresses.DeleteView.as_view()),
        name='wagtailaddresses_delete_address'
    ),
    # Address chooser URLs.
    url(
        r'^chooser/$',
        choosers.ChooseAddressView.as_view(),
        name='wagtailaddresses_address_chooser'
    ),
    url(
        r'^chooser/create/$',
        choosers.CreateAddressView.as_view(),
        name='wagtailaddresses_address_chooser_create'
    ),
    url(
        r'^chooser/(?P<pk>\d+)/$',
        choosers.ChosenAddressView.as_view(),
        name='wagtailaddresses_address_chosen'
    ),
    # Because address components are all derived from the same model, we only
    # need a single URL for choosing and editing them.
    url(
        r'^component-chooser/(?P<pk>\d+)/$',
        choosers.ChosenComponentView.as_view(),
        name='wagtailaddresses_component_chosen'
    ),
    url(
        r'^edit-component/(?P<pk>\d+)/$',
        choosers.UpdateComponentView.as_view(),
        name='wagtailaddresses_edit_component'
    ),
] + get_component_urls()
