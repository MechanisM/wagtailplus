"""
Contains generic class-based CRUD views.
"""
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.decorators.vary import vary_on_headers
from django.views.generic import CreateView as _CreateView
from django.views.generic import DeleteView as _DeleteView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import UpdateView as _UpdateView

from wagtail.wagtailadmin.edit_handlers import BaseObjectList
from wagtail.wagtailadmin.edit_handlers import extract_panel_definitions_from_model_class
from wagtail.wagtailadmin.forms import SearchForm
from wagtail.wagtailsearch.backends import get_search_backends


class IndexView(ListView):
    """
    Generic view class for listing existing instances.
    """
    page_kwarg          = 'p'
    paginate_by         = 20
    index_template      = None
    results_template    = None

    @vary_on_headers('X-Requested-With')
    def get(self, request, *args, **kwargs):
        """
        Processes GET request.

        :param request: the request instance.
        :rtype: django.http.HttpResponse.
        """
        return super(IndexView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Returns context data dictionary.

        :rtype: dict.
        """
        # Initialize common variables.
        queryset            = kwargs.pop('object_list', self.object_list)
        context_object_name = self.get_context_object_name(queryset)

        # Determine the desired ordering.
        ordering    = self.request.GET.get('ordering', '')
        fields      = [f.name for f in self.model._meta.fields]
        if not ordering.replace('-', '') in fields and hasattr(self.model, 'created_at'):
            ordering = '-created_at'
        if ordering:
            queryset = queryset.order_by(ordering)

        # Are we searching?
        is_searching    = False
        query_string    = None
        plural          = unicode(self.model._meta.verbose_name_plural)
        placeholder     = _(u'Search {0}'.format(plural))
        if 'q' in self.request.GET:
            form = SearchForm(self.request.GET, placeholder=placeholder)
            if form.is_valid():
                query_string    = form.cleaned_data['q']
                is_searching    = True
                queryset        = self.model.search(query_string)
        else:
            form = SearchForm(placeholder=placeholder)

        # Paginate the results.
        page_size   = self.get_paginate_by(queryset)
        page        = None
        if page_size:
            # Get paginated results.
            paginator, page, queryset, is_paginated = self.paginate_queryset(
                queryset,
                page_size
            )

        # Add common context data.
        kwargs.update({
            'object_list':  queryset,
            'ordering':     ordering,
            'query_string': query_string,
            'is_searching': is_searching,
            'page':         page,
        })

        # Add non-Ajax context data.
        if not self.request.is_ajax():
            kwargs.update({
                'search_form':  form,
                'popular_tags': self.model.popular_tags(),
            })

        if context_object_name is not None:
            kwargs.update({context_object_name: queryset})

        return kwargs

    def get_template_names(self):
        """
        Returns list of template names.

        :rtype: list.
        """
        names = [self.index_template]
        if self.request.is_ajax():
            names = [self.results_template]
        return names

class BaseFormView(FormView):
    """
    Generic view class for handling forms.
    """
    model = None

    def form_invalid(self, form):
        """
        Processes unsuccessful form submittal.

        :param form: the form instance.
        :rtype: django.http.HttpResponse.
        """
        # Add error message(s).
        default = _(u'The {0} could not be saved due to errors'.format(
            self.model._meta.verbose_name_raw.lower()
        ))

        for error in form.non_field_errors() or [default]:
            messages.error(self.request, error)

        # Return the response.
        return super(BaseFormView, self).form_invalid(form)

    def form_valid(self, form):
        """
        Processes successful form submittal.

        :param form: the form instance.
        :rtype: django.http.HttpResponse.
        """
        # Set the object from form data.
        self.object = form.save()

        # Reindex the instance to make sure all tags are indexed.
        for backend in get_search_backends():
            backend.add(self.object)

        # Add success message.
        messages.success(
            self.request,
            _(u"{0} '{1}' saved.").format(
                unicode(self.model._meta.verbose_name),
                unicode(self.object)
            )
        )

        # Redirect to success URL.
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        """
        Returns context data dictionary.

        :rtype: dict.
        """
        edit_handler_class  = self.get_edit_handler_class()
        instance            = self.object or self.model()
        form                = kwargs.get('form', self.get_form_class())

        kwargs.update({
            'edit_handler': edit_handler_class(instance=instance, form=form)
        })

        return kwargs

    def get_edit_handler_class(self):
        """
        Returns edit handler class for view model.

        :rtype: class.
        """
        # Custom class that skips adding missing fields, as we may want to
        # limit the number of fields presented to the user.
        class BaseChooserObjectList(BaseObjectList):
            def render_missing_fields(self):
                return ''
    
        def ChooserObjectList(children):
            return type('_ChooserObjectList', (BaseChooserObjectList,), {
                'children': children,
            })
    
        if hasattr(self.model, 'get_edit_handler'):
            handler_class = self.model.get_edit_handler()
        else:
            handler_class = ChooserObjectList(
                extract_panel_definitions_from_model_class(self.model)
            )

        # Return the edit handler class.
        return handler_class

    def get_form_class(self):
        """
        Returns form class for view model.

        :rtype: class.
        """
        return self.get_edit_handler_class().get_form_class(self.model)

class CreateView(BaseFormView, _CreateView):
    """
    Generic view class for adding new instances via edit handlers.
    """
    pass

class UpdateView(BaseFormView, _UpdateView):
    """
    Generic view class for editing existing instances via edit handlers.
    """
    pass

class DeleteView(_DeleteView):
    """
    Generic view class for deleting existing instances.
    """
    def delete(self, request, *args, **kwargs):
        """
        Deletes specified model instance.

        :param request: the request instance.
        :rtype: django.http.HttpResponse.
        """
        # Set object instance and redirect URL.
        self.object = self.get_object()
        success_url = self.get_success_url()

        # Delete the instance.
        self.object.delete()

        # Add success message.
        messages.success(
            self.request,
            _(u"{0} '{1}' deleted.").format(
                unicode(self.model._meta.verbose_name),
                unicode(self.object)
            )
        )

        # Return the response.
        return redirect(success_url)
