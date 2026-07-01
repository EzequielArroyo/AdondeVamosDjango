from .models import Activity
from django.shortcuts import redirect

class ActivityOwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        activity = self.get_object()

        if activity.creator != request.user:
            return redirect("activities:detail", pk=activity.pk)


        return super().dispatch(request, *args, **kwargs)