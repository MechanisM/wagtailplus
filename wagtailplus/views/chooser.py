"""
Contains generic classed-based chooser views.
"""
import json

from django.forms.models import modelform_factory
from django.utils.translation import ugettext as _
from django.views.generic import CreateView as _CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView as _UpdateView

from wagtail.wagtailadmin.forms import SearchForm
from wagtail.wagtailadmin.modal_workflow import render_modal_workflow
from wagtail.wagtailsearch.backends import get_search_backends


def get_model_permission(permission, model):
    """
    Returns specified permission string.

    :param permission: the permission string.
    :param model: the model instance.
    :rtype: str.
    """
    return '{0}.{1}_{2}'.format(
        model._meta.app_label,
        permission,
        model._meta.verbose_name_raw.lower()
    )

class ChooseView(ListView):
    """
    Generic view class for listing existing instances.
    """
    paginate_by         = 10
    form_class          = None
    chooser_template    = None
    results_template    = None
    chooser_javascript  = None

    def get_context_data(self, **kwargs):
        """
        Returns context data dictionary.

        :rtype: dict.
        """
        # Initialize common variables.
        createform          = None
        queryset            = kwargs.pop('object_list', self.object_list)
        context_object_name = self.get_context_object_name(queryset)

        # Are we searching?
        is_searching    = False
        query_string    = None
        plural          = unicode(self.model._meta.verbose_name_plural)
        placeholder     = _(u'Search {0}'.format(plural))
        if 'q' in self.request.GET:
            searchform = SearchForm(self.request.GET, placeholder=placeholder)
            if searchform.is_valid():
                query_string    = searchform.cleaned_data['q']
                is_searching    = True
                queryset        = self.model.search(
                    query_string,
                    filters=self.get_search_filters()
                )
        else:
            searchform  = SearchForm(placeholder=placeholder)

            # Add create form if user has "add" permission.
            permission_string = get_model_permission('add', self.model)
            if self.request.user.has_perm(permission_string):
                createform = self.get_form_class()

        # Paginate the results.
        page_size   = self.get_paginate_by(queryset)
        page        = None
        if page_size:
            # Get paginated results.
            paginator, page, queryset, is_paginated = self.paginate_queryset(
                queryset,
                page_size
            )

        kwargs.update({
            'object_list':  queryset,
            'createform':   createform,
            'searchform':   searchform,
            'is_searching': is_searching,
            'page':         page,
        })

        if context_object_name is not None:
            kwargs.update({context_object_name: queryset})

        return kwargs

    def get_form_class(self):
        """
        Returns form class for view model.

        :rtype: class.
        """
        form_class = self.form_class
        if not form_class:
            form_class = modelform_factory(self.model)
        return form_class

    def get_search_filters(self):
        """
        Returns dictionary of search filters.

        :rtype: dict.
        """
        return {}

    def get_template_names(self):
        """
        Returns list of template names.

        :rtype: list.
        """
        return [self.results_template]

    def render_to_response(self, context, **response_kwargs):
        """
        Returns rendered response instance.

        :param context: the context data dictionary.
        :rtype: django.http.HttpResponse.
        """
        is_searching = context.get('is_searching', False)

        if is_searching:
            return super(ChooseView, self).render_to_response(
                context,
                **response_kwargs
            )
        else:
            return render_modal_workflow(
                self.request,
                self.chooser_template,
                self.chooser_javascript,
                context
            )

class CreateView(_CreateView):
    """
    Generic view class for adding new instances.
    """
    chooser_template    = None
    chooser_javascript  = None
    chosen_javascript   = None

    def form_invalid(self, form):
        """
        Processes unsuccessful form submittal.

        :param form: the form instance.
        :rtype: django.http.HttpResponse.
        """
        return self.render_to_response(self.get_context_data(createform=form))

    def form_valid(self, form):
        """
        Processes successful form submittal.

        :param form: the form instance.
        :rtype: django.http.HttpResponse.
        """
        self.object = form.save()

        for backend in get_search_backends():
            backend.add(self.object)

        instance_json = json.dumps({
            'id':       self.object.id,
            'title':    unicode(self.object)
        })

        return render_modal_workflow(
            self.request,
            None,
            self.chosen_javascript,
            {'instance_json': instance_json}
        )

    def get_context_data(self, **kwargs):
        """
        Returns context data dictionary.

        :rtype: dict.
        """
        kwargs.update({
            'object_list':  self.get_queryset(),
            'searchform':   SearchForm(),
        })

        return kwargs

    def render_to_response(self, context, **response_kwargs):
        """
        Returns rendered response.

        :param context: the context data dictionary.
        :rtype: django.http.HttpResponse.
        """
        return render_modal_workflow(
            self.request,
            self.chooser_template,
            self.chooser_javascript,
            context,
        )

class ChosenView(DetailView):
    """
    Generic view class for choosing an existing instance.
    """
    chosen_javascript = None

    def render_to_response(self, context, **response_kwargs):
        """
        Returns rendered response.

        :param context: the context data dictionary.
        :rtype: django.http.HttpResponse.
        """
        instance        = self.get_object()
        instance_json   = json.dumps({
            'id':       instance.id,
            'title':    unicode(instance)
        })

        return render_modal_workflow(
            self.request,
            None,
            self.chosen_javascript,
            {'instance_json': instance_json}
        )

class UpdateView(_UpdateView):
    """
    Generic view class for editing existing instances.
    """
    chooser_javascript  = None
    chosen_javascript   = None

    def form_valid(self, form):
        """
        Processes successful form submittal.

        :param form: the form instance.
        :rtype: django.http.HttpResponse.
        """
        self.object = form.save()

        for backend in get_search_backends():
            backend.add(self.object)

        instance_json = json.dumps({
            'id':       self.object.id,
            'title':    unicode(self.object)
        })

        return render_modal_workflow(
            self.request,
            None,
            self.chosen_javascript,
            {'instance_json': instance_json}
        )

    def get_context_data(self, **kwargs):
        """
        Returns context data dictionary.

        :rtype: dict.
        """
        kwargs.update({
            'editform': self.get_form(self.get_form_class())
        })

        return super(UpdateView, self).get_context_data(**kwargs)

    def render_to_response(self, context, **response_kwargs):
        """
        Returns rendered response.

        :param context: the context data dictionary.
        :rtype: django.http.HttpResponse.
        """
        return render_modal_workflow(
            self.request,
            self.template_name,
            self.chooser_javascript,
            context,
        )
