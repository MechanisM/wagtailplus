"""
Contains view methods.
"""
from wagtail.wagtailadmin.modal_workflow import render_modal_workflow


def toggle_hallo_source(request):
    """
    Returns modal workflow HTTP response for hallo.js content.

    :rtype: django.http.HttpResponse.
    """
    return render_modal_workflow(
        request,
        'wagtailplus/toggle-hallo-source/update.html',
        'wagtailplus/toggle-hallo-source/update.js'
    )