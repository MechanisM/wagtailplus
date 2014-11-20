"""
Contains MailChimp page-related class definitions.
"""
import mailchimp
from collections import OrderedDict
from datetime import date

from django import forms
from django.conf import settings
from django.db import models
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailadmin.edit_handlers import FieldRowPanel
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel
from wagtailplus.forms import CountryField


def get_mailchimp_api():
    """
    Returns MailChimp API wrapper instance.

    :rtype: mailchimp.Mailchimp.
    """
    try:
        api_key = getattr(settings, 'MAILCHIMP_API_KEY', '')
        return mailchimp.Mailchimp(api_key)
    except:
        return None

def get_mailchimp_merge_vars(list_id):
    """
    Returns list of MailChimp merge variable dictionaries for list.

    :param list_id: the list ID.
    :rtype: list.
    """
    try:
        api     = get_mailchimp_api()
        result  = api.lists.merge_vars([list_id])
    
        return result['data'][0]['merge_vars']
    except:
        return []

def get_mailchimp_groupings(list_id):
    """
    Returns list of MailChimp grouping dictionaries for list.

    :param list_id: the list ID.
    :rtype: list.
    """
    try:
        api     = get_mailchimp_api()
        result  = api.lists.interest_groupings(list_id)

        return result
    except:
        return []

class MailChimpForm(forms.Form):
    """
    MailChimp list-based form class.
    """
    def __init__(self, merge_vars, groupings=[], *args, **kwargs):
        """
        Initailizes the form instance, adding fields for specified
        MailChimp merge variables and groupings.

        :param merge_vars: list of merge variable dictionaries.
        :param groupings: list of grouping dictionaries.
        """
        # Initialize the form instance.
        super(MailChimpForm, self).__init__(*args, **kwargs)

        # Add merge variable fields.
        for merge_var in merge_vars:
            for data in self.mailchimp_field_factory(merge_var).items():
                name, field = data
                self.fields.update({name: field})

        # Add grouping fields.
        for grouping in groupings:
            name    = grouping.get('name', '')
            field   = self.mailchimp_grouping_factory(grouping)
            self.fields.update({name: field})

    def mailchimp_field_factory(self, merge_var):
        """
        Returns a form field instance for specified MailChimp merge variable.

        :param merge_var: merge variable dictionary.
        :rtype: django.forms.Field.
        """
        fields  = OrderedDict()
        mc_type = merge_var.get('field_type', None)
        name    = merge_var.get('tag', '')
        kwargs  = {
            'label':        merge_var.get('name', None),
            'required':     merge_var.get('req', True),
            'initial':      merge_var.get('default', None),
            'help_text':    merge_var.get('helptext', None)
        }
    
        if mc_type == 'email':
            kwargs.update({'max_length': merge_var.get('size', None)})
            fields.update({name: forms.EmailField(**kwargs)})
    
        if mc_type == 'text':
            kwargs.update({'max_length': merge_var.get('size', None)})
            fields.update({name: forms.CharField(**kwargs)})
    
        if mc_type == 'number':
            fields.update({name: forms.IntegerField(**kwargs)})
    
        if mc_type == 'radio':
            kwargs.update({
                'choices':  ((x, x) for x in merge_var.get('choices', [])),
                'widget':   forms.RadioSelect
            })
            fields.update({name: forms.ChoiceField(**kwargs)})
    
        if mc_type == 'dropdown':
            kwargs.update({
                'choices':  ((x, x) for x in merge_var.get('choices', []))
            })
            fields.update({name: forms.ChoiceField(**kwargs)})
    
        if mc_type == 'date' or mc_type == 'birthday':
            fields.update({name: forms.DateField(**kwargs)})
    
        if mc_type == 'address':
            # Define keyword agruments for each charfield component.
            char_fields = [
                {
                    'name':         '{0}-addr1'.format(name),
                    'label':        'Address',
                    'required':     True,
                    'max_length':   70,
                },
                {
                    'name':         '{0}-addr2'.format(name),
                    'label':        'Address Line 2',
                    'required':     True,
                    'max_length':   70,
                },
                {
                    'name':         '{0}-city'.format(name),
                    'label':        'Address',
                    'required':     True,
                    'max_length':   40,
                },
                {
                    'name':         '{0}-state'.format(name),
                    'label':        'State/Province/Region',
                    'required':     True,
                    'max_length':   20,
                },
                {
                    'name':         '{0}-zip'.format(name),
                    'label':        'Zip Code',
                    'required':     True,
                    'max_length':   10,
                },
            ]
    
            # Add the address charfields.
            for kwargs in char_fields:
                field_name = kwargs.pop('name')
                fields.update({field_name: forms.CharField(**kwargs)})
    
            # Finally, add the address country field.
            name = '{0}-country'.format(name)
            fields.update({
                name: CountryField(label=_('Country'), initial='US')
            })
    
        if mc_type == 'zip':
            kwargs.update({'max_length': merge_var.get('size', None)})
            fields.update({name: forms.CharField(**kwargs)})
    
        if mc_type == 'phone':
            kwargs.update({'max_length': merge_var.get('size', None)})
            fields.update({name: forms.CharField(**kwargs)})
    
        if mc_type == 'url' or mc_type == 'imageurl':
            kwargs.update({'max_length': merge_var.get('size', None)})
            fields.update({name: forms.URLField(**kwargs)})
    
        return fields

    def mailchimp_grouping_factory(self, grouping):
        """
        Returns form field instance for specified MailChimp grouping.

        :param grouping: grouping dictionary.
        :rtype: django.forms.Field.
        """
        field_type  = grouping.get('form_field', None)
        name        = grouping.get('name', None)
        groups      = grouping.get('groups', [])
        choices     = ((x['name'], x['name']) for x in groups)
        kwargs      = {'label': name, 'choices': choices, 'required': False}

        if field_type == 'checkboxes':
            kwargs.update({'widget': forms.CheckboxSelectMultiple})
            return forms.MultipleChoiceField(**kwargs)

        if field_type == 'radio':
            kwargs.update({'widget': forms.RadioSelect})
            return forms.ChoiceField(**kwargs)

        if field_type == 'dropdown':
            kwargs.update({'widget': forms.Select})
            return forms.ChoiceField(**kwargs)

        if field_type == 'hidden':
            kwargs.update({'widget': forms.HiddenInput})
            return forms.ChoiceField(**kwargs)

class MailChimpView(FormView):
    """
    Displays and processes a form based on a MailChimp list.
    """
    form_class      = MailChimpForm
    page_instance   = None
    merge_vars      = None
    groupings       = None

    def get_clean_merge_vars(self, form):
        """
        Returns dictionary of MailChimp merge variables with cleaned
        form values.

        :param form: the form instance.
        :rtype: dict.
        """
        merge_vars = {'groupings': []}

        # Add merge variable values.
        for merge_var in self.get_merge_vars():
            mc_type = merge_var.get('field_type', '')
            name    = merge_var.get('tag', '')
            value   = form.cleaned_data.get(name, '')

            # Assemble address components into a single string value per
            # http://kb.mailchimp.com/lists/growth/format-list-fields#Address.
            if mc_type == 'address':
                values = []
                for f in ['addr1', 'addr2', 'city', 'state', 'zip', 'country']:
                    key = '{0}-{1}'.format(name, f)
                    val = form.cleaned_data.get(key)
                    if val:
                        values.append(val)
                value = '  '.join(values)

            # Convert date to string.
            if mc_type == 'date' and isinstance(value, date):
                value = value.strftime('%m/%d/%Y')

            # Convert birthday to string.
            if mc_type == 'birthday' and isinstance(value, date):
                value = value.strftime('%m/%d')

            merge_vars.update({name: value})

        # Add groupings.
        for grouping in self.get_groupings():
            id      = grouping.get('id', '')
            name    = grouping.get('name', '')
            groups  = form.cleaned_data.get(name, '')

            merge_vars['groupings'].append({
                'id':       id,
                'name':     name,
                'groups':   groups if type(groups) == list else [groups],
            })

        return merge_vars

    def get_context_data(self, **kwargs):
        """
        Returns view context data dictionary.

        :rtype: dict.
        """
        context = super(MailChimpView, self).get_context_data(**kwargs)
        context.update({'self': self.page_instance})
        return context

    def get_groupings(self):
        """
        Returns list of MailChimp grouping dictionaries.

        :rtype: dict.
        """
        if self.groupings is None:
            self.groupings = get_mailchimp_groupings(
                self.page_instance.list_id
            )

        return self.groupings

    def get_merge_vars(self):
        """
        Returns list of MailChimp merge variable dictionaries.

        :rtype: dict.
        """
        if self.merge_vars is None:
            self.merge_vars = get_mailchimp_merge_vars(
                self.page_instance.list_id
            )

        # If we don't have any merge variables to build a form from,
        # raise an HTTP 404 error.
        if not self.merge_vars:
            raise Http404

        return self.merge_vars

    def get_form(self, form_class=None):
        """
        Returns MailChimpForm instance.

        :param form_class: name of the form class to use.
        :rtype: wagtailplus.models.mailchimp_page.MailChimpForm.
        """
        merge_vars  = self.get_merge_vars()
        groupings   = self.get_groupings()

        return MailChimpForm(merge_vars, groupings, **self.get_form_kwargs())

    def get_template_names(self):
        """
        Returns list of available template names.

        :rtype: list.
        """
        return [self.page_instance.get_template(self.request)]

    def get_success_url(self):
        """
        Returns URL to redirect to upon successful form submittal.

        :rtype: str.
        """
        return self.page_instance.success_url.url

    def form_valid(self, form):
        """
        Subscribes to MailChimp list if form is valid.

        :param form: the form instance.
        """
        # Subscribe to the MailChimp list.
        api                 = get_mailchimp_api()
        clean_merge_vars    = self.get_clean_merge_vars(form)

        #raise Exception(clean_merge_vars)

        # Must have an email address.
        if api and 'EMAIL' in clean_merge_vars:
            api.lists.subscribe(
                self.page_instance.list_id,
                {'email': clean_merge_vars.pop('EMAIL')},
                merge_vars=clean_merge_vars,
                double_optin=self.page_instance.double_optin,
                update_existing=self.page_instance.update_existing,
                replace_interests=self.page_instance.replace_interests,
                send_welcome=self.page_instance.send_welcome
            )

        # Return HTTP response.
        return super(MailChimpView, self).form_valid(form)

class BaseMailChimpPage(models.Model):
    """
    Abstract MailChimp page definition.
    """
    list_id             = models.CharField(_('MailChimp List ID'), max_length=50, help_text=_('Enter the MailChimp list ID to use for this form'))
    double_optin        = models.BooleanField(_('Double Opt-In'), default=True, help_text=_('Use double opt-in process for new subscribers'))
    update_existing     = models.BooleanField(_('Update Existing'), default=True, help_text=_('Update existing information on re-subscription'))
    replace_interests   = models.BooleanField(_('Replace Interests'), default=True, help_text=_('Replace subscriber interests on re-subscription'))
    send_welcome        = models.BooleanField(_('Send Welcome'), default=True, help_text=_('Send welcome message to new subscribers'))
    success_url         = models.ForeignKey('wagtailcore.Page', verbose_name=_('Success URL'), related_name='+', help_text=_('Select the page that the user will be redirected to upon successful subscription'))

    class Meta(object):
        abstract = True

    def serve_as_mailchimp(self, request):
        """
        Serves the page as a MailChimpView.

        :param request: the request object.
        :rtype: django.http.HttpResponse.
        """
        view = MailChimpView.as_view(page_instance=self)
        return view(request)

BaseMailChimpPage.content_panels = [
    FieldPanel('title', classname='full title'),
    MultiFieldPanel([
        FieldPanel('list_id'),
        FieldPanel('double_optin'),
        FieldPanel('update_existing'),
        FieldPanel('replace_interests'),
        FieldPanel('send_welcome'),
    ], _(u'MailChimp Settings')),
    FieldPanel('success_url'),
]
