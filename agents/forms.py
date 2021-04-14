from django import forms
from core.models import Agent

class AgentModelForm(forms.ModelForm):
  class Meta:
    model = Agent
    fields = ('user',)