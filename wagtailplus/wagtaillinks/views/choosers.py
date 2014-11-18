"""
Contains address chooser view functions.
"""
from wagtail.wagtailadmin.modal_workflow import render_modal_workflow
from wagtail.wagtailsearch.backends import get_search_backends
from wagtailplus.views import chooser

from ..forms import ExternalLinkForm
from ..forms import EmailLinkForm
from ..models import Link


class LinkChooseView(chooser.ChooseView):
    """
    Link chooser view.
    """
    model               = Link
    results_template    = 'wagtaillinks/chooser/results.html'
    chooser_javascript  = 'wagtaillinks/chooser/chooser.js'

class LinkCreateView(chooser.CreateView):
    """
    Link create view.
    """
    model               = Link
    results_template    = 'wagtaillinks/chooser/results.html'
    chooser_javascript  = 'wagtaillinks/chooser/chooser.js'
    chosen_javascript   = 'wagtailadmin/chooser/chosen.js'

class LinkChosenView(chooser.ChosenView):
    """
    Link chosen view.
    """
    model               = Link
    chosen_javascript   = 'wagtailadmin/chooser/external_link_chosen.js'

class ExternalLinkChooseView(LinkChooseView):
    """
    External link chooser view.
    """
    form_class          = ExternalLinkForm
    chooser_template    = 'wagtaillinks/chooser/external-chooser.html'

    def get_queryset(self):
        """
        Returns queryset limited to external links.

        :rtype: django.db.models.query.QuerySet.
        """
        queryset    = super(ExternalLinkChooseView, self).get_queryset()
        queryset    = queryset.filter(link_type=Link.LINK_TYPE_EXTERNAL)

        return queryset

    def get_search_filters(self):
        """
        Returns dictionary of search filters.

        :rtype: dict.
        """
        return {'link_type': LINK_TYPE_EXTERNAL}

class EmailLinkChooseView(LinkChooseView):
    """
    Email link chooser view.
    """
    form_class          = EmailLinkForm
    chooser_template    = 'wagtaillinks/chooser/email-chooser.html'

    def get_queryset(self):
        """
        Returns queryset limited to external links.

        :rtype: django.db.models.query.QuerySet.
        """
        queryset    = super(EmailLinkChooseView, self).get_queryset()
        queryset    = queryset.filter(link_type=Link.LINK_TYPE_EMAIL)

        return queryset

    def get_search_filters(self):
        """
        Returns dictionary of search filters.

        :rtype: dict.
        """
        return {'link_type': LINK_TYPE_EMAIL}

class CreateAndEmbedLinkView(chooser.CreateView):
    """
    View that allows a link to be created and immediately embedded in
    a rich-text field.
    """
    model               = Link
    chooser_javascript  = 'wagtaillinks/chooser/chooser.js'
    chosen_javascript   = 'wagtailadmin/chooser/external_link_chosen.js'

    def get_queryset(self):
        """
        Returns queryset based on POST variables.

        :rtype: django.db.models.query.QuerySet.
        """
        queryset = super(CreateAndEmbedLinkView, self).get_queryset()

        if 'external_url' in self.request.POST:
            queryset = queryset.filter(link_type=Link.LINK_TYPE_EXTERNAL)
        if 'email' in self.request.POST:
            queryset = queryset.filter(link_type=Link.LINK_TYPE_EMAIL)

        return queryset

    def form_invalid(self, form):
        """
        Processes unsuccessful form submittal.

        :param form: the form instance.
        :rtype: django.http.HttpResponse.
        """
        # Remove unused field from form.
        if 'external_url' in self.request.POST:
            form.fields.pop('email', 0)
        if 'email' in self.request.POST:
            form.fields.pop('external_url', 0)

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

        return render_modal_workflow(
            self.request,
            None,
            self.chosen_javascript,
            {'url': self.object.url, 'link_text': self.object.title}
        )
