from typing import Any
import random
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from leads.models import Agent
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import OrganisorAndLoginrequireMixin
from .forms import AgentModelForm
# Create your views here.
class agent_list_view(OrganisorAndLoginrequireMixin,generic.ListView):
    template_name="agents/agents_list_view.html"
    context_object_name="agents"

    def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class agent_create_view(OrganisorAndLoginrequireMixin,generic.CreateView):
    template_name="agents/agent_create.html"
    form_class=AgentModelForm

    def get_success_url(self):
        return '/agents'
    
    def form_valid(self,form):
        user=form.save(commit=False)
        user.is_agent=True
        user.is_organisor=False
        user.set_password(f"{random.randint(0,1000000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )
        #agent.organisation=self.request.user.userprofile
        #agent.save()
        return super(agent_create_view,self).form_valid(form)
    
class agent_detail_view(OrganisorAndLoginrequireMixin,generic.DetailView):
    template_name="agents/agent_detail.html"
    context_object_name="agent"

    def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class agent_update_view(OrganisorAndLoginrequireMixin,generic.UpdateView):
    queryset=Agent.objects.all()
    form_class=AgentModelForm
    template_name="agents/agent_update.html"

    def get_success_url(self):
        return "/agents"
    
class agent_delete_view(OrganisorAndLoginrequireMixin,generic.DeleteView):
    template_name="agents/agent_delete.html"

    def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self):
        return "/agents"