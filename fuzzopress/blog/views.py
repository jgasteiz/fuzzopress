# -*- coding: utf-8 -*-
from datetime import date, datetime
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic.dates import MonthArchiveView
from django.views.generic import ListView, DetailView, View
from fuzzopress.blog.models import Post, NavItem, Widget, Tag
from fuzzopress.blog.utils import get_query as get_search_query


class CustomContextMixin(object):
    """ Same context data for every class view """
    paginate_by = settings.FUZZOPRESS_SETTINGS['entries_per_page']
    context_object_name = 'posts'
    template_name = 'blog/list.html'
    def get_context_data(self, **kwargs):
        context = super(CustomContextMixin, self).get_context_data(**kwargs)
        context.update({
            'navItems': NavItem.objects.all(),
            'widgets': Widget.objects.all(),
            'tags': Tag.objects.all(),
            'settings': settings.FUZZOPRESS_SETTINGS,
            'colour': settings.FUZZOPRESS_SETTINGS['colors'][datetime.today().weekday()]})
        return context


class BlogView(CustomContextMixin, ListView):
    """ Main blog view """
    def get_queryset(self):
        return Post.objects.published()


class TagView(CustomContextMixin, ListView):
    """ A tag posts """
    def get_queryset(self):
        return Post.objects.published().filter(mytags__name=self.kwargs['tag'])


class SearchView(CustomContextMixin, ListView):
    """ A search result posts """
    def get_queryset(self):
        query_string = self.kwargs['search']
        if query_string:
            entry_query = get_search_query(query_string, ['title', 'body',])
            return Post.objects.published().filter(entry_query)
        return Post.objects.published()


class PostView(CustomContextMixin, DetailView):
    """ A single post view """
    context_object_name = 'post'
    template_name = 'blog/detail.html'
    def get_object(self):
        return get_object_or_404(Post, slug=self.kwargs['slug'])


class ArchiveView(CustomContextMixin, ListView):
    """ For a month """
    context_object_name = 'archives'
    template_name = 'blog/archive.html'
    def get_queryset(self):
        archive = {}
        archive_qs = Post.objects.dates('published', 'month', order='DESC')
        for arch in archive_qs:
            year = arch.year
            month = arch.month
            try:
                archive[year][month - 1][1] = True
            except KeyError:
                # catch the KeyError, and set up list for that year
                archive[year] = [[date(year, m, 1), False] for m in xrange(1, 13)]
                archive[year][month - 1][1] = True
        return [sorted(archive.items(), reverse=True)]


class CustomDateMixin(CustomContextMixin, object):
    """ Same date_field and context_object_name for every Dated-class view """
    date_field = 'published'
    model = Post
    context_object_name = 'posts'


class ArchiveMonth(CustomDateMixin, MonthArchiveView):
    """ For a month """
    month_format = '%m'

