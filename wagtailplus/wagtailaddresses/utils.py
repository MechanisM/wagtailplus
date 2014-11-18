"""
Contains address-related utilities.
"""
from django.conf.urls import url

from .app_settings import ADDRESS_ATTR_MAP
from .views import choosers


def get_component_urls():
    """
    Returns list of address component URLs based on address attribute map.

    :rtype: list.
    """
    component_patterns = []
    
    for component, label in ADDRESS_ATTR_MAP.iteritems():
        label           = unicode(label)
        chooser_name    = 'wagtailaddresses_{0}_chooser'.format(component)
        create_name     = 'wagtailaddresses_{0}_create'.format(component)
        
        component_patterns.append(url(
            r'^{0}-chooser/$'.format(label.lower().replace(' ', '-')),
            choosers.ChooseComponentView.as_view(
                comp_type=label,
                chooser_name=chooser_name,
                create_name=create_name
            ),
            name=chooser_name
        ))
        
        component_patterns.append(url(
            r'^{0}-chooser/create/$'.format(label.lower().replace(' ', '-')),
            choosers.CreateComponentView.as_view(
                comp_type=label,
                chooser_name=chooser_name,
                create_name=create_name
            ),
            name=create_name
        ))

    return component_patterns