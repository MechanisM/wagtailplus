"""
Contains form class definitions.
"""
from django import forms

from .models import Link


class ExternalLinkForm(forms.ModelForm):
    """
    Form class for external link models.
    """
    class Meta(object):
        model   = Link
        fields  = ('title', 'external_url', 'tags')

class EmailLinkForm(forms.ModelForm):
    """
    Form class for email link models.
    """
    class Meta(object):
        model   = Link
        fields  = ('title', 'email', 'tags')