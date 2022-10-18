from django.http import HttpResponse
from django.shortcuts import render
from blog.models import BlogIndexPage, BlogPage, BlogPageTag
from taggit.models import TaggedItemBase,ItemBase
from taggit.models import Tag

def index(request):

    tag_list = BlogPageTag.objects.all()
    tagcontext = {'tag_list': tag_list}

    latest_question_list = BlogPage.objects.order_by('-webranking')[:16]
    # for blog in latest_question_list:
    #    print(blog)
    context = {'question_list': latest_question_list}

    latest_group_list = BlogIndexPage.objects.order_by('webgroupranking')[:12]
    groupcontext = {'latest_group_list': latest_group_list}

    return render(request, 'home/home_page.html',  {
        'question_list': latest_question_list,
        'latest_group_list': latest_group_list,
        'tag_list': tag_list
    })



