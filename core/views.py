from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import *
from .forms import * 

# Create your views here.

def lead_list(request):
  context = {
    "lead":Lead.objects.all()
  }
  return render(request, 'lead_list.html', context)


def lead_detail(request, id):
  context = {
    'leads':Lead.objects.get(id=id)
  }
  return render(request, 'lead_detail.html', context)


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


def lead_create(request):
  form = LeadModelForm()
  print(request.POST)
  if request.method == 'POST':
    form = LeadModelForm(request.POST or None)
    if form.is_valid():
      form.save()
      return redirect("/")
  return render(request, 'lead_create.html', {'form': form} )



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