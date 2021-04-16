
from django.contrib import admin
from django.urls import path, include
from core.views import LandingPageView, Signupview
from django.conf import  settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,PasswordResetCompleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", LandingPageView.as_view(), name="landing_page"),
    path("leads/", include("core.urls", namespace="core")),
    # all django built in view
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password-reset/", PasswordResetView.as_view(), name="password-reset"),
    path("password-reset-done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),  
    
    path("password-reset-complete/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # end of all djnago built in views
    path("signup/", Signupview.as_view(), name="signup"),
    path("agents/", include('agents.urls', namespace="agents")),
]
    

# for handling static files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    