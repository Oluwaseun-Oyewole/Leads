from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
  path('', views.LeadListView.as_view(), name="lead_list"),
  path("<int:pk>/", views.LeadDetailView.as_view(), name="lead_detail"),
  path("create/", views.LeadCreateView.as_view(), name="lead_create" ),
  path("<int:pk>/update/", views.LeadUpdateView.as_view(), name="lead_update"),
  path("<int:pk>/delete/", views.LeadDeleteView.as_view(), name="lead_delete"),
  path("<int:pk>/assign_agent/", views.AssignAgentView.as_view(), name="assign_agent"),
  path("categories/", views.CategoryListView.as_view(), name="category_list"), 
  path("category/create", views.CategoryCreateView.as_view(), name="category_create"),
  path("categories/<int:pk>/", views.CategoryDetailView.as_view(), name="category_detail"),  
  path("<int:pk>/category/", views.CategoryUpdateView.as_view(), name="category_update"),  
  path("<int:pk>/category_delete/", views.CategoryDeleteView.as_view(), name="category_delete"),  
]