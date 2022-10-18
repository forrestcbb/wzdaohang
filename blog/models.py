from django.db import models
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

# New imports added for ClusterTaggableManager, TaggedItemBase, MultiFieldPanel

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock



class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    webgroupranking = models.IntegerField(default=0, blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        # blogpages = self.get_children().live().order_by('-first_published_at')
        blogpages = self.get_children().live()

        # Paginate all posts by 2 per page
        paginator = Paginator(blogpages, 2)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)

        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle

        context['blogpages'] = posts
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('webgroupranking')
    ]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogTagIndexPage(Page):

    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context


class BlogPage(Page):
    date = models.DateField("发布日期：")
    intro = models.CharField(max_length=250)
    weburl = models.CharField("网址：", max_length=250, blank=True)
    # weburl2 = models.URLField("网址：", blank=True)
    # webranking = models.IntegerField(default=0, blank=True)
    body = RichTextField("正文：", blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('weburl'),
        # FieldPanel('weburl2'),
        # FieldPanel('webranking'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]


# －－－－－－－－－－－－－－－－－Github 周/月 代码 排行－－－－－－－－－－开始
'''
Github 周/月 代码 排行
'''


class GithubTrendingPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'GithubTrendingPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class GithubTrendingPage(Page):
    intro = models.CharField(max_length=250, blank=True)
    date = models.DateField("Post date")
    githubtags = ClusterTaggableManager(through=GithubTrendingPageTag, blank=True)
    # categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    body = StreamField([
        ('githubcodes', blocks.StructBlock([
            ('codename', blocks.CharBlock()),
            ('codeintro', blocks.CharBlock()),
            ('codeurl', blocks.CharBlock()),
            # ('codedetails', blocks.RichTextBlock()),
            # ('codephoto', ImageChooserBlock(required=False)),
        ])),
    ], use_json_field=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('githubtags'),
        ], heading="Github information"),
        FieldPanel('intro'),
        FieldPanel('date'),
        FieldPanel('body'),
    ]


class GithubIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        githubprojects = self.get_children().live().order_by('-first_published_at')

        context['githubprojects'] = githubprojects
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]


class GithubTrendingTagIndexPage(Page):

    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            githubpages = GithubTrendingPage.objects.filter(githubtags__name=tag)
        else:
            githubpages = GithubTrendingPage.objects.all()


        # Update template context
        context = super().get_context(request)
        context['githubpages'] = githubpages
        return context


# －－－－－－－－－－－－－－－－－Github 周/月 代码 排行－－－－－－－－－－结束

class WebPage(Page):
    intro = models.CharField(max_length=250)
    # tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    # categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    body = StreamField([
        ('project1', blocks.StructBlock([
            ('pname', blocks.CharBlock()),
            ('pintro', blocks.CharBlock()),
            ('purl', blocks.CharBlock()),
            ('photo', ImageChooserBlock(required=False)),
            ('biography', blocks.RichTextBlock()),
        ])),
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('webimage', ImageChooserBlock()),
    ], use_json_field=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        # MultiFieldPanel([
        #     FieldPanel('tags'),
        #     FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        # ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'
