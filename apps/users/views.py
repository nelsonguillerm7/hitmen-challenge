#  Django apps
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, FormView

# Local apps
from apps.users.forms import RegisterUserForm, HitmanBulkAssignedForm
from apps.users.models import User


class SignUpView(CreateView):
    """Class define register de user"""

    model = User
    form_class = RegisterUserForm
    template_name = "users/register.html"
    success_url = reverse_lazy("auth:login")

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Successfully registered")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "An error has occurred")
        return super().form_invalid(form)


class HitmanListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Class define list de hitman"""

    model = User
    template_name = "users/users_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.id != 1:
            queryset = queryset.filter(Q(id=user.id) | Q(manager=user))
        return queryset

    def has_permission(self):
        user = self.request.user
        return user.id == 1 or user.subordinates.all()


class HitmanDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Class define the detail hitman"""

    model = User
    template_name = "users/users_detail.html"

    def has_permission(self):
        user = self.request.user
        return user.id == 1 or user.subordinates.all()


class HitmanAddManagerCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    """Class define add hitman to managers"""

    form_class = HitmanBulkAssignedForm
    template_name = "users/user_bulk_form.html"
    success_url = reverse_lazy("auth:hitman_list")

    def form_valid(self, form):
        hitman = form.cleaned_data.get("hitman")
        manager = form.cleaned_data.get("manager")
        hitman = hitman.exclude(pk=manager.id)
        if hitman:
            hitman.update(manager=manager)
            manager.manager = None
            manager.save()
        messages.add_message(self.request, messages.SUCCESS, "Successfully assignment")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "An error has occurred")
        return super().form_invalid(form)

    def has_permission(self):
        return self.request.user.id == 1
