"""
Contains form class definitions.
"""
import pycountry
from collections import OrderedDict

from django import forms
from django.utils.translation import ugettext as _


class CountryField(forms.ChoiceField):
    """
    Renders a select element populated with world countries.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the instance.
        """
        # Build choices tuple from pycountry package.
        choices = (
            (c.alpha2, c.official_name)
            for c in pycountry.countries
            if hasattr(c, 'official_name')
        )

        kwargs.setdefault('choices', choices)
        super(CountryField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        """
        Returns internal class type.

        :rtype: str.
        """
        return 'ChoiceField'

class MailChimpForm(forms.Form):
    """
    MailChimp list-based form class.
    """
    def __init__(self, merge_vars, *args, **kwargs):
        """
        Initailizes the form instance, adding fields for specified
        MailChimp merge variables.

        :param merge_vars: list of merge variable dictionaries.
        """
        # Initialize the form instance.
        super(MailChimpForm, self).__init__(*args, **kwargs)

        # Add merge variable fields.
        for merge_var in merge_vars:
            for data in self.mailchimp_field_factory(merge_var).items():
                name, field = data
                self.fields.update({name: field})

    def mailchimp_field_factory(self, merge_var):
        """
        Returns a form field instance for specified MailChimp merge variable.

        :param merge_var: merge variable dictionary.
        :rtype: django.forms.Field.
        """
        fields  = OrderedDict()
        mc_type = merge_var.get('field_type', None)
        name    = merge_var.get('tag', '').lower()
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
