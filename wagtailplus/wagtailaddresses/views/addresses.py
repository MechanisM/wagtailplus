"""
Contains address view functions.
"""
from wagtailplus.views import crud

from ..models import Address


class IndexView(crud.IndexView):
    """
    Address index view.
    """
    model               = Address
    index_template      = 'wagtailaddresses/addresses/index.html'
    results_template    = 'wagtailaddresses/addresses/results.html'

class CreateView(crud.CreateView):
    """
    Address create view.
    """
    model           = Address
    template_name   = 'wagtailaddresses/addresses/add.html'
    success_url     = 'wagtailaddresses_index'

class UpdateView(crud.UpdateView):
    """
    Address update view.
    """
    model           = Address
    template_name   = 'wagtailaddresses/addresses/edit.html'
    success_url     = 'wagtailaddresses_index'

class DeleteView(crud.DeleteView):
    """
    Address delete view.
    """
    model           = Address
    template_name   = 'wagtailaddresses/addresses/confirm_delete.html'
    success_url     = 'wagtailaddresses_index'
