from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, ObjectList,
                                                TabbedInterface)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from greyjay.base import PaginatedListPageMixin


@python_2_unicode_compatible
class Organization(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(max_length=255)
    logo = models.ForeignKey(
        'images.AttributedImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return self.name


register_snippet(Organization)


Organization.panels = [
    FieldPanel('name'),
    FieldPanel('website'),
    ImageChooserPanel('logo'),
]


class EventListPage(PaginatedListPageMixin, Page):
    subpage_types = ['EventPage']

    events_per_page = models.IntegerField(default=20)
    counter_field_name = 'events_per_page'
    counter_context_name = 'events'

    @property
    def subpages(self):
        # Get list of live event pages that are descendants of this page
        subpages = EventPage.objects.live().descendant_of(self).order_by('-date')

        return subpages

    content_panels = Page.content_panels + [
        FieldPanel('events_per_page')
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


@python_2_unicode_compatible
class EventPage(Page):
    date = models.DateTimeField("Event Date")
    location = models.CharField(max_length=255)
    event_link = models.URLField(max_length=255)
    body = RichTextField()
    organization = models.ForeignKey(
        'Organization',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return "{}".format(
            self.title
        )

    content_panels = [
        FieldPanel("title"),
        FieldPanel("date"),
        FieldPanel("location"),
        FieldPanel("event_link"),
        FieldPanel("body"),
        SnippetChooserPanel('organization'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])
