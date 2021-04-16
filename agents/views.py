from django.shortcuts import render, reverse
from django.views import generic
from core.models import *
from .forms import  *
from .mixins import OrganiserAndLoginRequiredMixin
from django.core.mail import send_mail
import random
import string


def create_password_code():
  return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

class AgentListView(OrganiserAndLoginRequiredMixin, generic.ListView):
  template_name ="agents/agent_list.html"

  def get_queryset(self):
    # return Agent.objects.all()
    return Agent.objects.filter(organisation=self.request.user.userprofile)


class AgentCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm
    
    def get_success_url(self):
      return reverse("agents:agent_list")
      
    def form_valid(self, form):
      user = form.save(commit=False)
      user.is_agent = True
      user.is_organiser =  False
      user.set_password(create_password_code())
      user.save()
      Agent.objects.create(user=user, organisation=self.request.user.userprofile)
      # agent = form.save(commit=False)
      # agent.organisation = self.request.user.userprofile
      # agent.save()
      send_mail(
        subject="You are invited to be an agent",
        message = "You were added as an agent on CRM. Please come login to start working",
        from_email ="test@gmail.com",
        recipient_list = ["test123@gmail.com",]
      )
      return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganiserAndLoginRequiredMixin, generic.DetailView):
  template_name = "agents/agent_detail.html"
  context_object_name = "agent"
  
  def get_queryset(self):
    return Agent.objects.filter(organisation=self.request.user.userprofile)

class AgentUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
  template_name = "agents/agent_update.html"
  form_class = AgentModelForm
  # queryset = Agent.objects.all()
  
  def get_queryset(self):
      return Agent.objects.filter(organisation=self.request.user.userprofile)    

  def get_success_ulr(self):
    return reverse("agents:agent_list")
  
class AgentDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
  template_name ="agents/agent_delete.html"

  def get_queryset(self):
    return Agent.objects.filter(organisation=self.request.user.userprofile)

# for successful form submission
  def get_success_url(self):
    return reverse('agents:agent_list')