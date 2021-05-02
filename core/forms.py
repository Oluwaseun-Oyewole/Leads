from django import forms
from .models import * 
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model
from core.models import User

# User = get_user_model()

class LeadForm(forms.Form):
  first_name = forms.CharField(max_length=50)
  last_name = forms.CharField(max_length=50)
  age = forms.IntegerField(min_value=0)

class LeadModelForm(forms.ModelForm):
  class Meta:
    model = Lead
    fields = ('first_name', 'last_name', 'age', 'agent', 'description', 'phone_number', 'email')
    #  fields = ('first_name', 'last_ name', 'age', 'agent', 'organisation' )

class CustomUserCreationForm(UserCreationForm):
  class Meta:
    model = User
    fields = ("username",)
    field_classes ={"username":UsernameField}

class AssignAgentForm(forms.Form):
  agent=forms.ModelChoiceField(queryset=Agent.objects.none())
  
  # # populating agent or agents to the assigned view
  def __init__(self, *args, **kwargs):
    # print(kwargs)
    request = kwargs.pop("request")
    # print(request.user)
    agents = Agent.objects.filter(organisation=request.user.userprofile)
    super(AssignAgentForm, self).__init__(*args, **kwargs)
    self.fields["agent"].queryset=agents

class CategoryCreationForm(forms.ModelForm):
  class Meta:
    model= Category
    fields = "__all__"
    
class LeadCategoryUpdateForm(forms.ModelForm):
  class Meta:
    model = Lead
    fields = ("category" ,)

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  # agent = forms.ChoiceField(choices = (
  #   ("agent1", "agent1"),
  #   ("agent2", "agent2")
  # ))
    