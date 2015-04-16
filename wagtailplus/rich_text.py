"""
Contains rich-text related classes.
"""
import re

from django.utils.html import escape

from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.rich_text import EMBED_HANDLERS
from wagtail.wagtailcore.whitelist import Whitelister
from wagtail.wagtaildocs.models import Document
from wagtailplus.wagtaillinks.models import Link


def expand_db_attributes_for_model(model, attrs, for_editor):
    """
    Given a dictionary of attributes from the <a> tag, return
    the real HTML representation.

    :param model: the model class.
    :param attrs: dictionary of database attributes.
    :param for_editor: flag to display in editor or frontend.
    :rtype: str.
    """
    editor_attrs = ''

    try:
        obj = model.objects.get(id=attrs['id'])

        if for_editor:
            link_type       = model._meta.model.__name__.lower()
            editor_attrs    = 'data-linktype="{0}" data-id="{1}"'
            editor_attrs    = editor_attrs.format(link_type, obj.id)

        # Include title attribute for 508 compliance.
        return '<a {0} href="{1}" title="{2}">'.format(
            editor_attrs,
            escape(obj.url),
            obj.title
        )
    except model.DoesNotExist:
        return '<a>'

class BetterHandler(object):
    """
    Base handler class for embedded links to instances.
    """
    @staticmethod
    def get_db_attributes(tag):
        """
        Given an <a> tag that we've identified as a link embed, return a
        dictionary of the attributes we should have on the resulting
        <a> element.
        """
        return {'id': tag['data-id']}

    @classmethod
    def expand_db_attributes(cls, attrs, for_editor):
        """
        Given a dictionary of attributes from the <a> tag, return
        the real HTML representation.

        :param attrs: dictionary of database attributes.
        :param for_editor: flag to display in editor or frontend.
        :rtype: str.
        """
        return expand_db_attributes_for_model(cls.model, attrs, for_editor)

class BetterDocumentLinkHandler(BetterHandler):
    """
    BetterDocumentLinkHandler will be invoked whenever we encounter
    an element in HTML content with an attribute of
    data-embedtype="document". The resulting element in the database
    representation will be:
    <a data-linktype="document" data-id="42" href="[url]">.
    """
    model = Document

class BetterPageLinkHandler(BetterHandler):
    """
    BetterPageLinkHandler will be invoked whenever we encounter
    an element in HTML content with an attribute of
    data-embedtype="page". The resulting element in the database
    representation will be:
    <a data-linktype="page" data-id="42" href="[url]">.
    """
    model = Page

class BetterLinkHandler(BetterHandler):
    """
    LinkHandler will be invoked whenever we encounter an element in HTML 
    content with an attribute of data-embedtype="link". The resulting
    element in the database representation will be:
    <a data-linktype="link" data-id="42" href="[url]">.
    """
    model = Link

# Update link handlers.
LINK_HANDLERS = {
    'document': BetterDocumentLinkHandler,
    'page':     BetterPageLinkHandler,
    'link':     BetterLinkHandler,
}

class FlexibleDbWhitelister(Whitelister):
    """
    Prevents automatic replacement of 'DIV' tags with 'P' tags.
    """
    has_loaded_custom_whitelist_rules = False

    @classmethod
    def clean(cls, html):
        """
        Returns cleaned HTML.

        :param html: the HTML to clean.
        :rtype: str.
        """
        if not cls.has_loaded_custom_whitelist_rules:
            for fn in hooks.get_hooks('construct_whitelister_element_rules'):
                cls.element_rules = cls.element_rules.copy()
                cls.element_rules.update(fn())
            cls.has_loaded_custom_whitelist_rules = True

        return super(FlexibleDbWhitelister, cls).clean(html)

    @classmethod
    def clean_tag_node(cls, doc, tag):
        """
        Cleans specified tag node.

        :param doc: the document instance.
        :param tag: the tag instance.
        """
        if 'data-embedtype' in tag.attrs:
            embed_type = tag['data-embedtype']
            # Fetch the appropriate embed handler for this embedtype.
            embed_handler                   = EMBED_HANDLERS[embed_type]
            embed_attrs                     = embed_handler.get_db_attributes(tag)
            embed_attrs['embedtype']        = embed_type
            embed_tag                       = doc.new_tag('embed', **embed_attrs)
            embed_tag.can_be_empty_element  = True

            tag.replace_with(embed_tag)

        elif tag.name == 'a' and 'data-linktype' in tag.attrs:
            # First, whitelist the contents of this tag.
            for child in tag.contents:
                cls.clean_node(doc, child)

            link_type               = tag['data-linktype']
            link_handler            = LINK_HANDLERS['link']
            link_attrs              = link_handler.get_db_attributes(tag)
            link_attrs['linktype']  = link_type

            tag.attrs.clear()
            tag.attrs.update(**link_attrs)
        else:
            super(FlexibleDbWhitelister, cls).clean_tag_node(doc, tag)

FIND_A_TAG      = re.compile(r'<a(\b[^>]*)>')
FIND_EMBED_TAG  = re.compile(r'<embed(\b[^>]*)/>')
FIND_ATTRS      = re.compile(r'([\w-]+)\="([^"]*)"')

def extract_attrs(attr_string):
    """
    Helper method to extract tag attributes as a dictionary.
    Does not escape HTML entities!

    :param attr_string: string of attributes.
    :rtype: dict.
    """
    attributes = {}
    for name, val in FIND_ATTRS.findall(attr_string):
        attributes[name] = val
    return attributes

def expand_db_html(html, for_editor=False):
    """
    Expand database-representation HTML into proper HTML usable in either
    templates or the rich-text editor.

    :param html: the HTML to parse.
    :param for_editor: flag to display in editor or frontend.
    :rtype: str.
    """
    def replace_a_tag(m):
        attrs = extract_attrs(m.group(1))
        if 'linktype' not in attrs:
            # Return unchanged.
            return m.group(0)

        handler = LINK_HANDLERS[attrs['linktype']]
        return handler.expand_db_attributes(attrs, for_editor)

    def replace_embed_tag(m):
        attrs = extract_attrs(m.group(1))
        handler = EMBED_HANDLERS[attrs['embedtype']]
        return handler.expand_db_attributes(attrs, for_editor)

    html = FIND_A_TAG.sub(replace_a_tag, html)
    html = FIND_EMBED_TAG.sub(replace_embed_tag, html)

    return html
