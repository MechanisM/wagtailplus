"""

"""
import mailchimp
from collections import OrderedDict

from django import forms
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView

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
            fields.update({name: CountryField(initial='US')})
    
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
            kwargs.update({'widget': forms.MultipleChoiceField})

        if field_type == 'radio':
            kwargs.update({'widget': forms.RadioSelect})

        if field_type == 'dropdown':
            kwargs.update({'widget': forms.Select})

        if field_type == 'hidden':
            kwargs.update({'widget': forms.HiddenInput})

        return forms.ChoiceField(**kwargs)

class MailChimpView(CreateView):
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
            name    = merge_var.get('tag', '')
            value   = form.cleaned_data.get(name, '')

            merge_vars.update({name: value})

        # Add groupings.
        for grouping in get_mailchimp_groupings():
            id      = grouping.get('id', '')
            name    = grouping.get('name', '')
            groups  = form.cleaned_data.get(name, '')

            merge_vars['groupings'].append({id: id, name: name, groups: groups})

        return merge_vars

    def get_groupings(self):
        """
        Returns list of MailChimp grouping dictionaries.

        :rtype: dict.
        """
        if self.groupings is None:
            self.groupings = mailchimp_get_groupings(
                self.page_instance.list_id
            )

        return self.groupings

    def get_merge_vars(self):
        """
        Returns list of MailChimp merge variable dictionaries.

        :rtype: dict.
        """
        if self.merge_vars is None:
            self.merge_vars = mailchimp_get_merge_vars(
                self.page_instance.list_id
            )

        return self.merge_vars

    def get_form(self, form_class=None):
        """
        Returns MailChimpForm instance.

        :param form_class: name of the form class to use.
        :rtype: wagtailplus.models.mailchimp_page.MailChimpForm.
        """
        merge_vars  = self.get_merge_vars()
        groupings   = get_mailchimp_groupings(self.page_instance.list_id)

        return MailChimpForm(merge_vars, groupings, **self.get_form_kwargs())

    def form_valid(self, form):
        """
        Subscribes to MailChimp list if form is valid.

        :param form: the form instance.
        """
        # Subscribe to the MailChimp list.
        clean_merge_vars = self.get_clean_merge_vars(form)

        # Must have an email address.
        if 'EMAIL' in clean_merge_vars:
            api.lists.subscribe(
                self.page_instance.list_id,
                clean_merge_vars.pop('EMAIL'),
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
