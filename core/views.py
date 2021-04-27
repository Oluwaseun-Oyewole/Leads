from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from . models import *
from .forms import * 
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganiserAndLoginRequiredMixin


class Signupview(generic.CreateView):
  template_name ="registration/signup.html"
  form_class = CustomUserCreationForm

  def get_success_url(self):
    return reverse('login')


class LandingPageView(generic.TemplateView):
  template_name = "landing.html"

# def lead_list(request):
#   context = {
#     "leads":Lead.objects.all()
#   }
#   return render(request, 'lead_list.html', context)


class LeadListView(LoginRequiredMixin, generic.ListView):
  template_name ="lead_list.html"
  context_object_name = 'leads'
  
  def get_queryset(self):
    user = self.request.user
    if user.is_organiser:
      queryset= Lead.objects.filter(organisation=user.userprofile, agent__isnull=False)
    else:
      queryset=Lead.objects.filter(organisation=user.agent.organisation, agent__isnull=False)
      # flter for  tthe agent that is logged in 
      queryset = queryset.filter(agent__user=user)
    return queryset

# for updating  items in a generic class based view
  def get_context_data(self, **kwargs):
    context = super(LeadListView, self).get_context_data(**kwargs)
    user = self.request.user
    if user.is_organiser:
      queryset= Lead.objects.filter(organisation=user.userprofile, agent__isnull=True)
      context.update(
        {
          "unassigned_leads":queryset
        }
      )
    return context
  
  
# def lead_detail(request, id):
#   context = {
#     'leads':Lead.objects.get(id=id)
#   }
#   return render(request, 'lead_detail.html', context)


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
  template_name = 'lead_detail.html'
  context_object_name = 'leads'
  
  def get_queryset(self):
    user = self.request.user
    return  Lead.objects.filter(organisation=user.userprofile)
  
# for category
class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
  template_name = 'category_detail.html'
  context_object_name="category"
  
  def get_queryset(self):
    user = self.request.user 
    if user.is_organiser:
      queryset= Category.objects.filter(organisation=user.userprofile)
    else:
      queryset=Category.objects.filter(organisation=user.agent.organisation)
    return queryset


  def get_context_data(self, **kwargs):
      context = super(CategoryDetailView, self).get_context_data(**kwargs)
      # qs = Lead.objects.filter(category=self.get_object())
      # this syntax only works because we decaled a ForeignKey to the category model
      # self.get_object().lead_set.all()
      leads = self.get_object().leads.all()
      # print(qs)
      context.update({ "leads":leads})
      return context


# def lead_create(request):
#   form = LeadForm()
#   print(request.POST)
#   if request.method == 'POST':
#     form = LeadForm(request.POST or None)
#     if form.is_valid():
#       first_name = form.cleaned_data.get("first_name")
#       last_name = form.cleaned_data.get("last_name")
#       age = form.cleaned_data.get("age")
#       agent = Agent.objects.last()
#       lead = Lead.objects.create(first_name=first_name, last_name=last_name, age=age, agent=agent)
#       print('lead has been created')
#       return redirect("/")
#   return render(request, 'lead_create.html', {'form': form} )


# def lead_create(request):
#   form = LeadModelForm()
#   print(request.POST)
#   if request.method == 'POST':
#     form = LeadModelForm(request.POST or None)
#     if form.is_valid():
#       form.save()
#       return redirect("/")
#   return render(request, 'lead_create.html', {'form': form} )

class LeadCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
  template_name ="lead_create.html"
  form_class = LeadModelForm

# for successful form submission
  def get_success_url(self):
    return reverse('core:lead_list')
  
  def form_valid(self, form):
      user =form.save(commit=False)
      user.organisation=self.request.user.userprofile
      user.save()
      send_mail(
        subject="A lead has ben created", message="Go to the site  to see a new lead", from_email="test123@gmail.com", recipient_list=["test1234@gmail.com"]
        )
      return super(LeadCreateView, self).form_valid(form)

    
# def lead_update(request, id):
#   lead = Lead.objects.get(id=id)
#   form = LeadForm()
#   print(request.POST)
#   if request.method == 'POST':
#     form = LeadForm(request.POST or None)
#     if form.is_valid():
#       first_name = form.cleaned_data.get("first_name")
#       last_name = form.cleaned_data.get("last_name")
#       age = form.cleaned_data.get("age")
#       agent = Agent.objects.last()
#       lead.first_name = first_name
#       lead.last_name = last_name
#       lead.age = age
#       lead.save()
#       return redirect("/")
#     return render(request, 'lead_create.html', {'form': form, 'lead':lead} )
#   return render(request, 'lead_update.html', {'form': form, 'lead': lead} )

def lead_update(request, id):
  lead = Lead.objects.get(id=id)
  form = LeadModelForm(instance=lead)
  print(request.POST)
  if request.method == 'POST':
    form = LeadModelForm(request.POST or None, instance=lead)
    if form.is_valid():
      form.save()
      return redirect("/")
    return render(request, 'lead_create.html', {'form': form, 'lead':lead} )
  return render(request, 'lead_update.html', {'form': form, 'lead': lead} )

class LeadUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
  template_name ="lead_update.html"
  # queryset = Lead.objects.all()
  form_class = LeadModelForm

  def get_queryset(self):
    user = self.request.user
    return  Lead.objects.filter(organisation=user.userprofile)
  
# for successful form submission
  def get_success_url(self):
    return reverse('core:lead_list')
  
def lead_delete(request, id):
  lead = Lead.objects.get(id=id)
  lead.delete()
  return redirect("/")

class LeadDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
  template_name ="lead_delete.html"
  # queryset = Lead.objects.all()
  def get_queryset(self):
    user = self.request.user
    return  Lead.objects.filter(organisation=user.userprofile)
  
# for successful form submission
  def get_success_url(self):
    return reverse('core:lead_list')
  
class AssignAgentView(OrganiserAndLoginRequiredMixin, generic.FormView):
  template_name = 'assign_agent.html'
  form_class = AssignAgentForm
  
  # for passing extra information into the form
  def get_form_kwargs(self, **kwargs):
    kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
    kwargs.update({
      "request":self.request
    })
    return kwargs
    
  def get_success_url(self):
    return reverse('core:lead_list')

  def form_valid(self, form):
    agent = form.cleaned_data['agent']
    lead = Lead.objects.get(pk=self.kwargs["pk"])
    lead.agent = agent
    lead.save()
    return super(AssignAgentView, self).form_valid(form)

# Category section

class CategoryListView(LoginRequiredMixin, generic.ListView):
  template_name= "category_list.html"
  context_object_name = "category_list"
  
  def get_queryset(self):
    user = self.request.user
    if user.is_organiser:
      queryset= Category.objects.filter(organisation=user.userprofile)
    else:
      queryset=Category.objects.filter(organisation=user.agent.organisation)
    return queryset
  
  def get_context_data(self, **kwargs):
      context = super(CategoryListView, self).get_context_data(**kwargs)
      user = self.request.user
      if user.is_organiser:
        queryset= Lead.objects.filter(organisation=user.userprofile)
      else:
        queryset= Lead.objects.filter(organisation=user.userprofile)
      context.update({ "unassigned_lead_count":queryset.filter(category__isnull=True).count() })
      return context


class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
  template_name ="category_update.html"
  form_class = LeadCategoryUpdateForm

  def get_queryset(self):
    user = self.request.user
    return Lead.objects.filter(organisation=user.userprofile)
  
  def get_success_url(self):
      return reverse('core:lead_detail', kwargs={"pk":self.get_object().id})
