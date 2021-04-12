from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
# from django.contrib.auth import get_user_model
# User = get_user_model()


SOURCE_CHOICES = (
  ("Youtube", "Youtube"), 
  ("Google", "Google"), 
  ("Newsletter", 'Newsletter')
)

class User(AbstractUser):
  pass

class Lead(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  age = models.IntegerField(default=0)
  agent = models.ForeignKey('Agent', on_delete=models.CASCADE)
  
  
  def get_absolute_url(self):
    return reverse('core:lead_detail', kwargs={'pk': self.pk})
  
  def __str__(self):
    return f'{self.first_name} {self.last_name}'

class Agent(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  
  def __str__(self):
    return self.user.username