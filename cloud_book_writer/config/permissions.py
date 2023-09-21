from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginAuthor(LoginRequiredMixin):
    """Verify that the current user is authenticated and is Author"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.roles == "Author":
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()


class CustomLoginCollaborator(LoginRequiredMixin):
    """Verify that the current user is authenticated and is Collaborator"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.roles != "Author":
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()
