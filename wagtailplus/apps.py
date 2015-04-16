"""
Contains application configuration.
"""
from django.apps import AppConfig
from django.db import models


class WagtailPlusAppConfig(AppConfig):
    name            = 'wagtailplus'
    label           = 'wagtailplus'
    verbose_name    = 'Wagtail Plus'

    def _set_get_template(self):
        """
        Sets correct "get_template" method for CustomTemplateMixin models.
        """
        from .mixins import CustomTemplateMixin

        for model in models.get_models():
            if issubclass(model, CustomTemplateMixin):
                model.get_template = CustomTemplateMixin.get_template

    def ready(self):
        """
        Finalizes application setup.
        """
        self._set_get_template()