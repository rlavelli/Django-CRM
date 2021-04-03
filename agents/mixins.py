from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class OrganizerAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated. And is an organizer. """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organizer:
            return redirect('leads:lead-list')
        return super().dispatch(request, *args, **kwargs)

# TEST
class LoggedinMixin(AccessMixin):
    """Verify that the user is logged. """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('leads:lead-list')
        return super().dispatch(request, *args, **kwargs)