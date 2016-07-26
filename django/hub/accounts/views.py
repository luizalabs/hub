# coding: utf-8
import logging

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import (
    CreateView, DetailView, ListView, TemplateView, UpdateView
)

from awards.forms import AccountAwardForm

from forms import ProfileUpdateForm
from models import Account


logger = logging.getLogger('accounts.views')


class AccountListView(ListView):
    queryset = Account.objects.order_by('name')
    template_name = 'accounts/account_list.html'


class AccountDetailView(DetailView):
    model = Account
    template_name = 'accounts/account_detail.html'
    slug_field = 'email'

    def get_context_data(self, **kwargs):
        context = super(AccountDetailView, self).get_context_data(**kwargs)
        context['user_is_ancestor'] = self.request.user.is_ancestor_of(self.get_object())
        return context


class AccountUpdateView(UpdateView):
    model = Account
    form_class = ProfileUpdateForm
    template_name = 'accounts/account_update.html'
    slug_field = 'email'
    success_url = reverse_lazy('accounts:account_list')

    def get_queryset(self):
        qs = super(AccountUpdateView, self).get_queryset()

        if not self.request.user.is_superuser:
            qs = qs.filter(email__exact=self.request.user.email)
        return qs

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(AccountUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class OrganogramView(TemplateView):
    template_name = 'accounts/organogram.html'

    def get_context_data(self, **kwargs):
        context = super(OrganogramView, self).get_context_data(**kwargs)
        context['people'] = Account.objects.order_by('name')
        return context


class AccountAwardCreateView(CreateView):
    form_class = AccountAwardForm
    template_name = 'awards/account_award_add.html'
    slug_field = 'email'

    def dispatch(self, *args, **kwargs):
        self.account = Account.objects.get(
            email=kwargs['slug'],
        )
        return super(AccountAwardCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        award = form.save(commit=False)
        award.account = self.account
        award.awarded_by = self.request.user
        award.save()

        return HttpResponseRedirect(
            reverse('accounts:account_detail', kwargs={
                'slug': self.account.email,
            })
        )
