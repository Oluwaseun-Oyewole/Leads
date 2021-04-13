
from django.contrib import admin
from django.urls import path, include
from core.views import LandingPageView
from django.conf import  settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", LandingPageView.as_view(), name="landing_page"),
    path("leads/", include("core.urls", namespace="core"))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)