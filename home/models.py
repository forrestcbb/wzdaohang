from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from taggit.models import Tag

from blog.models import BlogPage
from blog.models import GithubTrendingPage


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        # blogpages = self.get_children().live().order_by('-first_published_at')
        blogpages = self.get_children().live().in_menu()
        context['pages'] = blogpages

        webtags = Tag.objects.all()
        pagetags = BlogPage.tags.all()
        githubtags = GithubTrendingPage.githubtags.all()

        githubpage=GithubTrendingPage.objects.all()[:1]
        # for item in blogpages:
        #     if item.title == 'Github weekly monthly trending':
        #         githubpage = item




        context['webtags'] = webtags
        context['pagetags'] = pagetags
        context['githubtags'] = githubtags
        context['githubpage'] = githubpage
        return context
