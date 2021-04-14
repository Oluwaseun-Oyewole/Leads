from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import *
from .forms import  *

class AgentListView(LoginRequiredMixin, generic.ListView):
  template_name ="agents/agent_list.html"

  def get_queryset(self):
    return Agent.objects.all()

class AgentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm
    
    def get_success_url(self):
      return reverse("agents:agent_list")
    
    def form_valid(self, form):
      agent = form.save(commit=False)
      agent.organisation = self.request.user.userprofile
      agent.save()
      return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(LoginRequiredMixin, generic.DetailView):
  template_name = "agents/agent_detail.html"
  context_object_name = "agent"
  
  def get_queryset(self):
    return Agent.objects.all()
    
class AgentUpdateView(LoginRequiredMixin, generic.UpdateView):
  template_name = "agents/agent_update.html"
  form_class = AgentModelForm
  queryset = Agent.objects.all()
  
  def get_success_ulr(self):
    return reverse("agents:agent_list")
  
  
class AgentDeleteView(LoginRequiredMixin, generic.DeleteView):
  template_name ="agents/agent_delete.html"
  queryset =Agent.objects.all()

# for successful form submission
  def get_success_url(self):
    return reverse('agents:agent_list')