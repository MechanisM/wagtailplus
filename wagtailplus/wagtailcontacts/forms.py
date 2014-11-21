"""
Contains form class definitions.
"""
from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta(object):
        model   = Contact
        fields  = ('name', 'website', 'email', 'telephone', 'tags')