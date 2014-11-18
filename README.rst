.. image:: http://i.imgur.com/UPmcr7m.png

Wagtail Plus
============

Wagtail Plus is a collection of add-ons for `Wagtail CMS <https://github.com/torchbox/wagtail>`_, featuring:

* Link (external and email) storage and management
* Contact storage and management
* GeoDjango-enabled address storage and management
* Event storage and management

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
