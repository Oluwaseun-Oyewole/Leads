from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
  path('', views.lead_list),
  path("<id>/", views.lead_detail),
  path("create/", views.lead_create),
  path("<id>/update/", views.lead_update)
]