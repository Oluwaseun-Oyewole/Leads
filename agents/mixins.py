from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class OrganiserAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organiser:
          return redirect("core:lead_list")
        return super().dispatch(request, *args, **kwargs)