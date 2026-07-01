
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.activities.models import Activity
from apps.participations.models import Participation

from .forms import ProfileForm, UserForm
from .forms import RegisterForm
from .models import Profile


class RegisterView(CreateView):

    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:profile_update")

    def form_valid(self, form):                 #Re defino porque necesito auto login
        response = super().form_valid(form)     #utilizo el metodo original
        login(self.request, self.object)        #agrego el auto-login
        return response                         #El metodo original ya redirecciona a success_url
       
class MyProfileView(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = "users/my_profile.html"
    
    def get_object(self):
        return self.request.user.profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        context["created_activities"] = Activity.objects.filter(
            creator=user
        ).select_related("creator")

        context["participations"] = Activity.objects.filter(
            participations__user=user
        ).select_related("creator")

        return context
    
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "users/profile.html"
    
    def get_object(self):
        return get_object_or_404(Profile, user_id=self.kwargs["user_id"])
    
class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = "users/profile_update.html"

    def get(self, request):
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

        return render(
            request,
            self.template_name,
            {
                "user_form": user_form,
                "profile_form": profile_form,
            },
        )

    def post(self, request):

        user_form = UserForm(request.POST, instance=request.user)

        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if (user_form.is_valid() and profile_form.is_valid()):

            user_form.save()
            profile = profile_form.save(commit=False) #lo trae a memoria sin guardar en bd
            profile.update_completion_status()
            profile.save()
            return redirect("users:my_profile")

        return render(
        request,
        self.template_name,
        {
            "user_form": user_form,
            "profile_form": profile_form,
        }
    )    