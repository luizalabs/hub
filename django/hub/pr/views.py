# coding: utf-8
import logging

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import AddQuestionForm, PressReleaseForm, QuestionUpdateForm
from .models import PressRelease, Question

logger = logging.getLogger('pr.views')


class PressReleaseListView(ListView):
    queryset = PressRelease.objects.order_by('-created_at')
    template_name = 'pr/pressrelease_list.html'


class PressReleaseDetailView(DetailView):
    queryset = PressRelease.objects.all()
    template_name = 'pr/pressrelease_detail.html'


class PressReleaseCreateView(CreateView):
    form_class = PressReleaseForm
    template_name = 'pr/pressrelease_add.html'
    success_url = reverse_lazy('pr:pressrelease_list')

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super(PressReleaseCreateView, self).form_valid(form)


class PressReleaseUpdateView(UpdateView):
    model = PressRelease
    form_class = PressReleaseForm
    template_name = 'pr/pressrelease_update.html'

    def dispatch(self, request, *args, **kwargs):
        press_release = self.get_object()

        is_superuser = request.user.is_superuser
        is_owner = request.user.id == press_release.added_by_id

        if not is_superuser and not is_owner:
            return HttpResponseForbidden(u'Você não pode editar esse item')

        return super(PressReleaseUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'pr:pressrelease_detail',
            kwargs={'pk': self.object.id}
        )


class QuestionCreateView(CreateView):
    form_class = AddQuestionForm
    template_name = 'pr/question_add.html'

    def get(self, *args, **kwargs):
        self.press_release = PressRelease.objects.get(
            pk=kwargs['pressrelease_id'],
        )
        return super(QuestionCreateView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.press_release = PressRelease.objects.get(
            pk=kwargs['pressrelease_id'],
        )
        return super(QuestionCreateView, self).post(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuestionCreateView, self).get_context_data(**kwargs)
        context['press_release'] = self.press_release
        return context

    def form_valid(self, form):
        question = form.save(commit=False)
        question.press_release = self.press_release
        question.author = self.request.user
        question.save()

        return HttpResponseRedirect(
            reverse('pr:pressrelease_detail', kwargs={'pk': question.press_release.id})
        )


class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionUpdateForm
    template_name = 'pr/question_update.html'

    def get_success_url(self):
        return reverse(
            'pr:pressrelease_detail',
            kwargs={'pk': self.get_object().press_release.id}
        )
