# coding: utf-8
import logging
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from forms import TeamCreateForm, TeamUpdateForm
from models import Team


logger = logging.getLogger('teams.views')


class TeamListView(ListView):
    # order is important (using ttag `ifchanged`)
    queryset = Team.objects.order_by('area__name', 'name')
    template_name = 'teams/team_list.html'


class TeamDetailView(DetailView):
    queryset = Team.objects.all()
    template_name = 'teams/team_detail.html'


class TeamUpdateView(UpdateView):
    form_class = TeamUpdateForm
    queryset = Team.objects.all()
    template_name = 'teams/team_update.html'
    success_url = reverse_lazy('teams:team_list')

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return Team.objects.all()
        return Team.objects.filter(id=self.request.user.team_id)


class TeamCreateView(CreateView):
    admin_required = True
    form_class = TeamCreateForm
    template_name = 'teams/team_create.html'
    success_url = reverse_lazy('teams:team_list')
