"""
Contains address chooser view functions.
"""
from wagtailplus.views import chooser

from ..forms import AddressForm
from ..forms import AddressComponentForm
from ..models import Address
from ..models import AddressComponent


class ChooseAddressView(chooser.ChooseView):
    """
    Address choose view.
    """
    model               = Address
    form_class          = AddressForm
    results_template    = 'wagtailaddresses/address-chooser/results.html'
    chooser_template    = 'wagtailaddresses/address-chooser/chooser.html'
    chooser_javascript  = 'wagtailaddresses/address-chooser/chooser.js'

class CreateAddressView(chooser.CreateView):
    """
    
    """
    model               = Address
    form_class          = AddressForm
    chooser_template    = 'wagtailaddresses/address-chooser/chooser.html'
    chooser_javascript  = 'wagtailaddresses/address-chooser/chooser.js'
    chosen_javascript   = 'wagtailaddresses/address-chooser/chosen.js'

class ChosenAddressView(chooser.ChosenView):
    """
    Address chosen view.
    """
    model               = Address
    chosen_javascript   = 'wagtailaddresses/address-chooser/chosen.js'

class BaseComponentView(object):
    """
    Base address component view.
    """
    model           = AddressComponent
    form_class      = AddressComponentForm
    comp_type       = None
    chooser_name    = None
    create_name     = None

    def get_context_data(self, **kwargs):
        """
        Returns context data dictionary.

        :rtype: dict.
        """
        kwargs.update({
            'verbose_name': self.comp_type,
            'chooser_name': self.chooser_name,
            'create_name':  self.create_name,
        })

        return super(BaseComponentView, self).get_context_data(**kwargs)

    def get_queryset(self):
        """
        Returns queryset, filtered by component type.

        :rtype: django.db.models.query.QuerySet.
        """
        queryset    = super(BaseComponentView, self).get_queryset()
        queryset    = queryset.filter(type=self.comp_type)

        return queryset

    def get_search_filters(self):
        """
        Returns dictionary of search filters for component type.

        :rtype: dict.
        """
        return {'type': self.comp_type}

class ChooseComponentView(BaseComponentView, chooser.ChooseView):
    """
    Address component choose view.
    """
    results_template    = 'wagtailaddresses/component-chooser/results.html'
    chooser_template    = 'wagtailaddresses/component-chooser/chooser.html'
    chooser_javascript  = 'wagtailaddresses/component-chooser/chooser.js'

class CreateComponentView(BaseComponentView, chooser.CreateView):
    """
    Address component create view.
    """
    chooser_template    = 'wagtailaddresses/component-chooser/chooser.html'
    chooser_javascript  = 'wagtailaddresses/component-chooser/chooser.js'
    chosen_javascript   = 'wagtailaddresses/component-chooser/chosen.js'

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.

        :rtype: dict.
        """
        kwargs = super(CreateComponentView, self).get_form_kwargs()
        kwargs.update({'instance': self.model(type=self.comp_type)})
        return kwargs

class ChosenComponentView(chooser.ChosenView):
    """
    Address component chosen view.
    """
    model               = AddressComponent
    chosen_javascript   = 'wagtailaddresses/component-chooser/chosen.js'

class UpdateComponentView(BaseComponentView, chooser.UpdateView):
    """
    Address component update view.
    """
    template_name       = 'wagtailaddresses/component-chooser/edit.html'
    chooser_javascript  = 'wagtailaddresses/component-chooser/chooser.js'
    chosen_javascript   = 'wagtailaddresses/component-chooser/chosen.js'

    def get_queryset(self):
        """
        Returns queryset of all address components.

        :rtype: django.db.models.query.QuerySet.
        """
        return AddressComponent.objects.all()
