# coding: utf-8
import logging

from urlparse import urljoin

from django.conf import settings
from django.contrib import messages
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import (CreateView, UpdateView, BaseFormView,
                                       DeleteView)

from forms import (
    ProjectForm,
    ChangelogForm,
    SendMailChangelogForm,
    SendSlackForm
)
from models import Project, Changelog


logger = logging.getLogger('projects.views')


class ProjectListView(ListView):
    queryset = Project.objects.order_by('name')
    template_name = 'projects/project_list.html'

    def get_queryset(self):
        return super(ProjectListView, self).get_queryset().filter(parent=None)


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    slug_field = 'name'

    def get_initial(self):
        last_changelog = self.project.changelog_set.order_by('-id').first()

        if last_changelog:
            email_recipients = last_changelog.email_recipients
        else:
            email_recipients = ', '.join(settings.DEFAULT_CHANGELOG_RECIPIENTS)

        return {
            'email_recipients': email_recipients,
            'email_subject': u'Changelog - {}'.format(self.project.name),
            'channel': '#changelogs',
        }

    def get_form_kwargs(self):
        return {'initial': self.get_initial()}

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        self.project = self.object
        form_kwargs = self.get_form_kwargs()
        context['send_mail_form'] = SendMailChangelogForm(**form_kwargs)
        context['send_slack_form'] = SendSlackForm(**form_kwargs)
        return context


class ProjectUpdateView(UpdateView):
    form_class = ProjectForm
    template_name = 'projects/project_form.html'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return Project.objects.all()
        return Project.objects.filter(team=self.request.user.team)

    def get_success_url(self):
        return reverse('projects:project_detail', args=(self.get_object().id,))


class ProjectCreateView(CreateView):
    form_class = ProjectForm
    template_name = 'projects/project_form.html'

    def form_valid(self, form):
        project = form.save(commit=False)
        project.added_by = self.request.user
        project.save()
        form.save_m2m()

        return HttpResponseRedirect(
            reverse('projects:project_detail', kwargs={'pk': project.pk})
        )

    def get_initial(self):
        return {
            'parent': self.kwargs.get('project_pk')
        }


class ChangelogCreateView(CreateView):
    form_class = ChangelogForm
    model = Changelog

    def dispatch(self, *args, **kwargs):
        self.project = Project.objects.get(
            pk=kwargs['project_id'],
        )
        return super(ChangelogCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ChangelogCreateView, self).get_context_data(**kwargs)
        context['project'] = self.project
        return context

    def get_initial(self):
        last_changelog = self.project.changelog_set.order_by('-id').first()
        if last_changelog:
            email_recipients = last_changelog.email_recipients
        else:
            email_recipients = ', '.join(settings.DEFAULT_CHANGELOG_RECIPIENTS)

        return {
            'email_recipients': email_recipients,
            'email_subject': u'Changelog - {}'.format(self.project.name),
            'description': u'# Versão X.Y.Z\n\n* ...\n* ...'
        }

    def form_valid(self, form):
        changelog = form.save(commit=False)
        changelog.project = self.project
        changelog.added_by = self.request.user
        changelog.save()

        if form.cleaned_data['send_mail'] is True:
            changelog.send_mail()

        return HttpResponseRedirect(
            reverse('projects:project_detail', kwargs={
                'pk': self.project.id,
            })
        )


class ChangelogUpdateView(UpdateView):
    model = Changelog
    form_class = ChangelogForm
    pk_url_kwarg = 'changelog_id'

    def dispatch(self, *args, **kwargs):
        self.changelog = get_object_or_404(
            Changelog,
            pk=kwargs['changelog_id'],
            email_sent=False,
        )
        return super(ChangelogUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        changelog = form.save(commit=False)
        changelog.added_by = self.request.user
        changelog.save()

        if form.cleaned_data['send_mail'] is True:
            changelog.send_mail()

        return HttpResponseRedirect(
            reverse('projects:project_detail', kwargs={
                'pk': self.changelog.project.id,
            })
        )

    def get_context_data(self, **kwargs):
        context = super(ChangelogUpdateView, self).get_context_data(**kwargs)
        context['project'] = self.object.project
        return context


class ChangelogDeleteView(DeleteView):
    form_class = ChangelogForm
    pk_url_kwarg = 'changelog_id'
    http_method_names = ['post', 'delete']
    queryset = Changelog.objects.filter(email_sent=False)

    def get_success_url(self):
        return reverse('projects:project_detail', kwargs={
            'pk': self.object.project_id,
        })


class ChangelogSendMailView(BaseFormView):
    form_class = SendMailChangelogForm
    http_method_names = ['post', ]

    def dispatch(self, *args, **kwargs):
        self.changelog = get_object_or_404(
            Changelog,
            pk=kwargs['changelog_id'],
        )
        return super(ChangelogSendMailView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ChangelogSendMailView, self).get_form_kwargs()
        kwargs['instance'] = self.changelog
        return kwargs

    def form_valid(self, form):
        changelog = form.save(commit=False)
        changelog.added_by = self.request.user
        changelog.save()
        changelog.send_mail()

        return HttpResponseRedirect(
            reverse('projects:project_detail', kwargs={
                'pk': self.changelog.project.id,
            })
        )

    def form_invalid(self, form):
        messages.error(
            self.request,
            u'Informações inválidas para enviar e-mail.'
        )
        return HttpResponseRedirect(
            reverse('projects:project_detail', kwargs={
                'pk': self.changelog.project.id,
            })
        )


class ChangelogSendSlackView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('changelog_id')
        changelog = get_object_or_404(Changelog, pk=pk)

        channels = request.POST.get('channel', '#changelogs').split(',')

        for channel in channels:
            channel = channel.strip()
            kwargs = {
                'channel': channel,
                'username': request.user.name,
                'text': u'{}\n{}'.format(
                    changelog.project,
                    changelog.description
                ), 'icon_emoji': ':memo:',
            }

            try:
                changelog.send_slack(**kwargs)
            except Exception as e:
                logger.exception(u'Failed to send changelog')
                logger.exception(e, exc_info=True)

        return HttpResponseRedirect(
            reverse('projects:project_detail', kwargs={
                'pk': changelog.project.id,
            })
        )
