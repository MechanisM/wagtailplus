"""

"""
import mailchimp

from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.views.generic import FormView
from django.utils.translation import ugettext_lazy as _

from localflavor.us.forms import USPhoneNumberField

__ALL__ = [
    'MailChimpPage',
]

class MailChimpForm(forms.Form):
    """

    """
    EMAIL_TYPES = (
        (_('HTML'), _('HTML')),
        (_('Text'), _('Text'))
    )

    list            = None
    merge_vars      = {}
    groupings       = []

    # Default MailChimp options.
    list_id             = None
    double_optin        = True
    update_existing     = True
    replace_interests   = True
    send_welcome        = True

    def __init__(self, *args, **kwargs):
        """
        Initializes instance with MailChimp data.
        """
        # Set custom attributes. These are stored with the MailChimp page model
        # and must be removed from the keyword arguments dictionary before
        # initializing the form.
        mailchimp_attrs = [
            'list_id',
            'double_optin',
            'update_existing',
            'replace_interests',
            'send_welcome',
        ]

        # Set attribute values from keyword arguments.
        for attr in mailchimp_attrs:
            setattr(self, attr, kwargs.pop(attr))

        # Initialize form instance with remaining arguments.
        super(MailChimpForm, self).__init__(*args, **kwargs)

        # Establish the MailChimp connection.
        conn        = mailchimp.utils.get_connection()
        self.list   = conn.get_list_by_id(self.list_id)

        # Add MailChimp fields.
        self.add_merge_fields()
        self.add_grouping_fields()

    def get_merge_vars(self):
        """
        Returns merge vars dictionary with cleaned form data.

        :rtype: dict.
        """
        merge_vars = {}
        # Get cleaned form data for each tag.
        for tag, name in self.merge_vars.iteritems():
            merge_vars[tag] = self.cleaned_data[name] # pylint: disable=E1101
        # Add any groupings.
        merge_vars['groupings'] = self.get_groupings_merge_var()
        # Return the merge vars dictionary.
        return merge_vars

    def get_groupings_merge_var(self):
        """
        Returns groupings merge var with cleaned form data.

        :rtype: list.
        """
        groupings = []
        for grouping in self.groupings:
            groupings.append({
                'id':       grouping.get('id', ''),
                'name':     grouping.get('name', ''),
                'groups':   self.cleaned_data.get(grouping.get('name', '')) # pylint: disable=E1101
            })
        return groupings

    def add_grouping_fields(self):
        """
        Adds choice fields for MailChimp list interest groupings.
        """
        try:
            for grouping in self.list.list_interest_groupings():
                group_id    = grouping.get('id', '')
                name        = grouping.get('name', '')
                field_type  = grouping.get('form_field', '')
                choices     = ((x['name'], x['name']) for x in grouping.get('groups', []))

                self.groupings.append({
                    'id':           group_id,
                    'name':         name,
                    'field_type':   field_type
                })

                if field_type == 'radio':
                    widget = forms.RadioSelect
                else:
                    continue

                self.fields.insert(     # pylint: disable=E1101
                    len(self.fields),   # pylint: disable=E1101
                    name,
                    forms.ChoiceField(label=name, widget=widget, choices=choices)
                )
        except mailchimp.chimpy.chimpy.ChimpyException:
            pass

    def add_merge_fields(self):
        """
        Adds fields for MailChimp list merge vars.
        """
        # Map field type names to classes.
        field_types = {
            'email':    forms.EmailField,
            'phone':    USPhoneNumberField,
            'text':     forms.CharField,
        }

        # Create fields from list merge vars.
        for merge in self.list.get_merges():
            typ     = merge.get('field_type')
            tag     = merge.get('tag')
            kwargs  = {
                'label':        merge.get('name'),
                'max_length':   merge.get('size'),
                'initial':      merge.get('default'),
                'required':     merge.get('req'),
                'help_text':    merge.get('helptext'),
            }

            # Only add if field type is defined.
            if typ in field_types:
                self.fields.insert(             # pylint: disable=E1101
                    len(self.fields),           # pylint: disable=E1101
                    merge.get('tag').lower(),
                    field_types[typ](**kwargs)  # pylint: disable=W0142
                )
                self.merge_vars[tag] = tag.lower()

    def clean(self):
        """
        Checks for required values and subscribes to the list.

        :raises django.core.exceptions.ValidationError: if subscription fails.
        """
        # Make sure that we have all required data first.
        cleaned = self.cleaned_data.keys()              # pylint: disable=E1101
        for label, field in self.fields.iteritems():    # pylint: disable=E1101
            if field.required and label not in cleaned:
                return
        try:
            self.subscribe()
        except Exception:
            msg = _('Your request cannot be completed at this time.')
            raise ValidationError(msg)

    def subscribe(self):
        """
        Subscribes to mailing list with cleaned form data.
        """
        self.list.subscribe(
            self.cleaned_data.get('email'), # pylint: disable=E1101
            self.get_merge_vars(),
            double_optin        = self.double_optin,
            update_existing     = self.update_existing,
            replace_interests   = self.replace_interests,
            send_welcome        = self.send_welcome
        )

class MailChimpView(FormView): # pylint: disable=R0901
    """

    """
    page_instance   = None
    form_class      = MailChimpForm

    def get_context_data(self, **kwargs):
        """
        Adds page instance as "self" context variable.

        :rtype: dict.
        """
        context = super(MailChimpView, self).get_context_data(**kwargs)
        context.update({'self': self.page_instance})
        return context

    def get_form_kwargs(self):
        """
        Adds MailChimp-specific arguments to form initialization
        keyword arguments.

        :rtype: dict.
        """
        kwargs = super(MailChimpView, self).get_form_kwargs()
        kwargs.update({
            'list_id':              self.page_instance.list_id,
            'double_optin':         self.page_instance.double_optin,
            'update_existing':      self.page_instance.update_existing,
            'replace_interests':    self.page_instance.replace_interests,
            'send_welcome':         self.page_instance.send_welcome
        })
        return kwargs

    def get_success_url(self):
        """
        Returns the supplied success URL.

        :rtype: str.
        """
        return self.page_instance.success_url.url

    def get_template_names(self):
        """
        Returns list of available template names.

        :rtype: list.
        """
        default = self.page_instance.get_template_name()
        return [default]

class MailChimpPage(models.Model):
    """

    """
    list_id             = models.CharField(_('MailChimp List ID'), max_length=50, help_text=_('Enter the MailChimp list ID to use for this form'))
    double_optin        = models.BooleanField(_('Double Opt-In'), default=True, help_text=_('Use double opt-in process for new subscribers'))
    update_existing     = models.BooleanField(_('Update Existing'), default=True, help_text=_('Update existing information on re-subscription'))
    replace_interests   = models.BooleanField(_('Replace Interests'), default=True, help_text=_('Replace subscriber interests on re-subscription'))
    send_welcome        = models.BooleanField(_('Send Welcome'), default=True, help_text=_('Send welcome message to new subscribers'))
    success_url         = models.ForeignKey('wagtailcore.Page', verbose_name=_('Success URL'), related_name='+', help_text=_('Select the page that the user will be redirected to upon successful subscription'))

    class Meta(object):
        abstract            = True
        verbose_name        = _('MailChimp Form Page')
        verbose_name_plural = _('MailChimp Form Pages')

    def serve(self, request):
        """
        Serves the page as an HTTP response.

        :param request: the request object.
        :rtype: django.http.HttpResponse.
        """
        view = MailChimpView.as_view(page_instance=self)
        return view(request)
