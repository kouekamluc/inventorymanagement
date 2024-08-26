from django.shortcuts import render

# Create your views here.

from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .models import UserProfile
from django.contrib import messages






class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'user_management/user_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.userprofile


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'user_management/user_profile_form.html'
    fields = ['bio', 'location', 'birth_date', 'department', 'employee_id']
    success_url = reverse_lazy('user_profile')

    def get_object(self):
        return self.request.user.userprofile
    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        user.first_name = self.request.POST.get('first_name')
        user.last_name = self.request.POST.get('last_name')
        user.email = self.request.POST.get('email')
        user.save()
        messages.success(self.request, 'Profile updated successfully.')
        return response

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'user_management/password_change.html'
    success_url = reverse_lazy('user_profile_edit')
    
    def form_valid(self, form):
        messages.success(self.request, 'Your password was successfully updated!')
        return super().form_valid(form)