"""
Contains mixin classes.
"""
import collections

from django.db import models
from django.utils.functional import cached_property

from taggit.models import TaggedItem
from wagtail.wagtailadmin.taggable import TagSearchable
from wagtail.wagtailcore.models import Page


class CustomTemplateMixin(models.Model):
    """
    Allows per-instance templates.
    """
    template_name = models.CharField('Template Name', max_length=100, blank=True)

    class Meta(object):
        abstract = True

    def get_template(self, request, *args, **kwargs):
        """
        Returns template name.

        :param request: the request instance.
        :rtype: str.
        """
        if self.template_name:
            return self.template_name

        # Fall back to standard page method.
        return Page.get_template(self, request, *args, **kwargs)

class RelatedItemsMixin(object):
    """
    Allows access to other instances (pages and generic) that
    are related by tags.
    """
    def _get_related_score(self, item):
        """
        Returns the number of tags that specified item instance
        has in common with this instance.

        :param item: the related item instance.
        :rtype: int.
        """
        return len(list(set(self.tags.all()).intersection(item.tags.all())))

    def _get_pages(self, tag):
        """
        Returns a set of unique pages for specified tag.

        :param: tag object.
        :rtype: set.
        """
        related = []
        exclude = [self.pk]

        for child in self.get_children().all():
            exclude.append(child.pk)

        for model in models.get_models():
            # Is model derived from Page class?
            derived = issubclass(model, Page) and model != Page

            # Does model have a "tags" attribute?
            if derived and hasattr(model, 'tags'):
                mgr = model.objects.live()

                for item in mgr.filter(tags__in=[tag]).exclude(pk__in=exclude):
                    item.related_score  = self._get_related_score(item)
                    related.append(item)

        return set(related)

    def _get_generic_items(self, tag):
        """
        Returns a set of unique generic items for specified tag.

        :param: tag object.
        :rtype: set.
        """
        related = []

        for generic in TaggedItem.objects.filter(tag__in=[tag]):
            item = generic.content_object
            item.related_score = self._get_related_score(item)
            related.append(item)

        return set(related)

    @property
    def related_by_type(self):
        """
        Returns a dictionary of related items keyed by model's verbose name.

        :rtype: dict.
        """
        related = collections.defaultdict(list)

        for item in self.related:
            key = unicode(item._meta.verbose_name_plural)
            related[key].append(item)

        return collections.OrderedDict(
            sorted(related.items(), key=lambda x: x[0])
        )

    @property
    def related_by_score(self):
        """
        Returns a list of related items sorted by related score.

        :rtype: list.
        """
        return sorted(self.related, key=lambda x: x.related_score)

    @cached_property
    def related(self):
        """
        Returns a list of items related by tags.

        :rtype: list.
        """
        related = []

        for tag in self.tags.all():
            # Add Generic items.
            related += self._get_generic_items(tag)

            # Add pages.
            related += self._get_pages(tag)

        # Sort items by name.
        return sorted(set(related), key=lambda x: str(x))

class BasePageMixin(CustomTemplateMixin, RelatedItemsMixin, TagSearchable):
    """
    Base mixin class for website pages (CustomTemplateMixin,
    RelatedItemsMixin, and TagSearchable).
    """
    class Meta(object):
        abstract = True

    @cached_property
    def live_children(self):
        """
        Returns queryset of live child instances.

        :rtype: django.db.models.query.QuerySet.
        """
        child_pks = self.get_children().values_list('pk', flat=True)

        return Page.objects.live().filter(pk__in=child_pks)

    @cached_property
    def tag_names(self):
        """
        Returns list of associated tag names without hyphens.

        :rtype: list.
        """
        return [tag.name.replace('-', ' ') for tag in self.tags.all()]
