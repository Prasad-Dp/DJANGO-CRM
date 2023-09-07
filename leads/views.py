from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from .models import Lead,Agent,Category
from .forms import LeadForm,LeadModelForm,CustomUserCreationForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorAndLoginrequireMixin

def landing_page(request):
    return render(request, "landing.html")

class landing_view(generic.TemplateView):
    template_name="landing.html"


def leads_list(request):
    leads=Lead.objects.all()
    context={
        'leads':leads
    }
    return render(request,"leads/leads_list_view.html",context)

class leads_list_view(LoginRequiredMixin, generic.ListView):
    template_name="leads/leads_list_view.html"
    context_object_name="leads"

    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            quaryset=Lead.objects.filter(organisation=user.userprofile,agent__isnull=False)
        else:
            quaryset=Lead.objects.filter(organisation=user.agent.organisation)
            quaryset=quaryset.filter(agent__user=user)
        return quaryset
    
    def get_context_data(self,**kwargs):
        context=super(leads_list_view,self).get_context_data(**kwargs)
        user=self.request.user
        if user.is_organisor:
            quaryset=Lead.objects.filter(organisation=user.userprofile,agent__isnull=True)
        context.update({
            "unassigned_leads":quaryset
        })
        return context
    
    

def leads_view(request,pk):

    leads=Lead.objects.get(id=pk)
    context={
        'leads':leads
    }
    return render(request,'leads/leads_detail_view.html',context)

class leads_detail_view(LoginRequiredMixin,generic.DetailView):
    template_name="leads/leads_detail_view.html"
    context_object_name="leads"

    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            quaryset=Lead.objects.filter(organisation=user.userprofile)
        else:
            quaryset=Lead.objects.filter(organisation=user.agent.organisation)
            quaryset=quaryset.filter(agent__user=user)
        return quaryset

def leads_create(request):
    form=LeadForm()
    if request.method=="POST":
        form=LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context={
        'form':form
    }
    return render(request,"leads/leads_create.html",context)

class leads_create_view(OrganisorAndLoginrequireMixin,generic.CreateView):
    template_name="leads/leads_create.html"
    form_class=LeadForm
    
    def get_success_url(self):
        return "/leads"

def lead_update(request,pk):
    lead=Lead.objects.get(id=pk)
    form=LeadModelForm()
    if request.method =="POST":
        form=LeadModelForm(request.POST)
        if form.is_valid():
            frist_name=form.cleaned_data['frist_name']
            last_name=form.cleaned_data['last_name']
            age=form.cleaned_data['age']
            lead.frist_name=frist_name
            lead.last_name=last_name
            lead.age=age
            lead.save()
            return redirect("/leads")
    context={
        'form':form,
        'leads':lead
    }
    return render(request,"leads/leads_update.html",context)

class lead_update_view(OrganisorAndLoginrequireMixin,generic.UpdateView):
    template_name="leads/leads_update.html"
    form_class=LeadForm

    def get_queryset(self):
        user=self.request.user
        quaryset=Lead.objects.filter(organisation=user.userprofile)
        return quaryset

    def get_success_url(self):
        return "/leads"
    
def lead_delete(request,pk):
    lead=Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")

class lead_delete_view(OrganisorAndLoginrequireMixin,generic.DeleteView):
    template_name="leads/leads_delete.html"

    def get_queryset(self):
        user=self.request.user
        quaryset=Lead.objects.filter(organisation=user.userprofile)
        return quaryset


    def get_success_url(self):
        return "/leads"
    
class registration(generic.CreateView):
    template_name="registration/registration.html"
    form_class=CustomUserCreationForm

    def get_success_url(self):
        return "/login"
    
class CategoryListView(LoginRequiredMixin,generic.ListView):
    template_name="leads/category_list.html"
    context_object_name="category"

    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            queryset=Category.objects.filter(organisation=user.userprofile)

        else:
            queryset=Category.objects.filter(organisation=user.agent.organisation)
        return queryset
    
    def get_context_data(self, **kwargs):
        context= super(CategoryListView,self).get_context_data(**kwargs)
        user=self.request.user
        if user.is_organisor:
            queryset=Lead.objects.filter(organisation=user.userprofile)

        else:
            queryset=Lead.objects.filter(organisation=user.agent.organisation)

        context.update({
            'unassigned':queryset.filter(category__isnull=True).count()
        })
        return context
    
class categoryDetailView(LoginRequiredMixin,generic.DetailView):
    template_name="leads/category_detail.html"
    context_object_name="category"

    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            queryset=Category.objects.filter(organisation=user.userprofile)

        else:
            queryset=Category.objects.filter(organisation=user.agent.organisation)
        return queryset