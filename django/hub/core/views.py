# coding: utf-8
import json

from django.http import HttpResponse
from django.views.generic import ListView
from django.shortcuts import resolve_url as r

from accounts.models import Account
from projects.models import Project
from taggit.models import Tag
from utils.security import ajax_basic_protection


class TagsListView(ListView):
    template_name = 'core/tags_list.html'

    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
        accounts = kwargs.pop('accounts', self.accounts)
        projects = kwargs.pop('projects', self.projects)

        context = {
            'paginator': None,
            'page_obj': None,
            'is_paginated': False,
            'accounts': accounts,
            'projects': projects,
            'tag': self.tag_name,
        }
        context.update(kwargs)
        return context

    def get(self, request, *args, **kwargs):
        self.tag_id = self.kwargs.get('tag_id')
        self.accounts = Account.objects.filter(tags=self.tag_id)
        self.projects = Project.objects.filter(tags=self.tag_id)

        # this attribute is used by other methods and need be created here
        self.object_list = None

        try:
            tag = Tag.objects.get(id=self.tag_id)
            self.tag_name = tag.name
        except:
            self.tag_name = u'Não existente!'

        context = self.get_context_data()
        return self.render_to_response(context)


@ajax_basic_protection
def get_tags_json(request, *args, **kwargs):
    """
    Get all tags
    """
    tags = Tag.objects.all()
    tag_list = []
    for tag in tags:
        url = r('core:tags_list', tag_id=tag.id)
        tag_list.append({
            "tag": tag.name,
            "weight": tag.taggit_taggeditem_items.count(),
            "url": url,
        })

    return HttpResponse(
        json.dumps(tag_list), content_type="application/json")
