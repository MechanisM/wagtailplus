.. image:: http://i.imgur.com/UPmcr7m.png

Wagtail Plus
============

Wagtail Plus is a collection of add-ons for `Wagtail CMS <https://github.com/torchbox/wagtail>`_, featuring:

* Link (external and email) storage and management, fully integrated with page editor.
* Event storage and management, including support for pattern-based repeating events.
* GeoDjango-enabled address storage and management (defaults to standard classes if :code:`django.contrib.gis` is not installed).
* Simple contact storage and management.

Wagtail Plus also includes the following abstract models:

* :code:`BaseMailChimpPage`: stores MailChimp settings with page and renders/processes a subscription form based on a MailChimp list.
* :code:`BaseMultiBlockPage`: stores multiple HTML blocks with page, each of which can be assigned CSS styles.

Installation
~~~~~~~~~~~~
Add Wagtail Plus to INSTALLED_APPS in your project's settings **BEFORE** the Wagtail CMS apps, then add the individual Wagtail Plus apps:

::

    INSTALLED_APPS = (
        ...
        # Add wagtailplus before wagtail, as it includes admin tempaltes.
        'wagtailplus',
        ...
        'wagtailplus.wagtailaddresses',
        'wagtailplus.wagtailcontacts',
        'wagtailplus.wagtailevents',
        'wagtailplus.wagtaillinks',
    )

Documentation
~~~~~~~~~~~~~
Coming soon!