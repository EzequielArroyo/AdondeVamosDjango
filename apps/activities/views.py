from multiprocessing import context
from winreg import CreateKey

from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from apps.activities.forms import ActivityForm
from apps.activities.mixins import ActivityOwnerRequiredMixin

from .models import Activity
from .exceptions import *


class ActivityListView(ListView):

    model = Activity
    template_name = "activities/list.html"
    context_object_name = "activities"
    
class ActivityCreateView(LoginRequiredMixin, CreateView):
    form_class = ActivityForm
    template_name = "activities/create.html"
    
    def form_valid(self, form):
        activity = form.save(commit=False)
        activity.creator = self.request.user
        activity.save()
        return redirect("activities:detail", pk=activity.pk)
    
class ActivityUpdateView(LoginRequiredMixin, ActivityOwnerRequiredMixin, UpdateView):

    model = Activity
    form_class = ActivityForm
    template_name = "activities/edit.html"

    def get_success_url(self):
        return reverse_lazy("activities:detail", kwargs={"pk": self.object.pk})
    
    
class ActivityDetailView(DetailView):

    model = Activity
    template_name = "activities/detail.html"
    context_object_name = "activity"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context["is_creator"] = self.object.is_creator(self.request.user)
            context["is_participant"] = self.object.is_participant(self.request.user)
        else:
            context["is_creator"] = False
            context["is_participant"] = False
        return context

class ActivityJoinView(LoginRequiredMixin, View):
    def post(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        try:
            activity.join(request.user)
            messages.success(request,"You joined the activity.")
        except ActivityFullError:
            messages.error(request, "This activity is already full.")
        except ActivityClosedError:
            messages.error(request, "This activity is closed.")
        except AlreadyParticipantError:
            messages.warning(request, "You have already joined this activity.")
        return redirect("activities:detail", pk=pk)

class ActivityLeaveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        try:
            activity.leave(request.user)
            messages.success(request, "You left the activity.")
        except ActivityFinishedError:
            messages.error(request, "This activity has already finished.")
        except NotParticipantError:
            messages.warning(request, "You are not a participant of this activity.")
        return redirect("activities:detail", pk=pk)
    
class MyActivitiesView(LoginRequiredMixin, ListView):

    model = Activity
    template_name = "activities/my_activities.html"
    context_object_name = "activities"

    def get_queryset(self):
        return self.request.user.created_activities.all()
    
class MyJoinedActivitiesView(LoginRequiredMixin, ListView):

    model = Activity
    template_name = "activities/my_activities.html"
    context_object_name = "activities"

    def get_queryset(self):
        return Activity.objects.filter(participations__user=self.request.user)
    
class ActivityDeleteView(
    LoginRequiredMixin,
    ActivityOwnerRequiredMixin,
    DeleteView,
):
    model = Activity
    success_url = reverse_lazy("activities:list")