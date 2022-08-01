# Django Core
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView

# Local apps
from apps.hits.forms import HitForm, BulkAssignForm
from apps.hits.models import Hit
from apps.users.models import User


class HitListView(LoginRequiredMixin, ListView):
    """Class define list hits"""

    model = Hit
    template_name = "hits/hit_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.pk != 1:
            subordinates = user.subordinates.all()
            if subordinates:
                return queryset.filter(Q(assigned=user) | Q(assigned__in=subordinates))
            return queryset.filter(assigned=user)
        return queryset


class HitDetailView(LoginRequiredMixin, DetailView):
    """Class define detail hits"""

    model = Hit
    template_name = "hits/hit_detail.html"


class HitCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Class define create hit"""

    model = Hit
    form_class = HitForm
    template_name = "hits/hit_form.html"
    success_url = reverse_lazy("hits:hit_list")

    def has_permission(self):
        user = self.request.user
        return user.id == 1 or user.subordinates.all()

    def get_initial(self):
        initial = super().get_initial()
        initial["creator"] = self.request.user
        return initial

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        return super().form_valid(form)


class HitUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Hit
    form_class = HitForm
    template_name = "hits/hit_form.html"
    success_url = reverse_lazy("hits:hit_list")

    def has_permission(self):
        instance = self.get_object()
        if instance.state != Hit.HitState.ASSIGNED:
            return False
        return True

    def get_initial(self):
        initial = super().get_initial()
        initial["creator"] = self.request.user
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.get_object().assigned.state == User.UserState.INACTIVE:
            form["target"].disabled = True
            form["description"].disabled = True
        return form


class HitBulkUpdateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    """Class define bulk hits"""

    form_class = BulkAssignForm
    template_name = "hits/hit_bulk_form.html"
    success_url = reverse_lazy("hits:hit_list")

    def form_valid(self, form):
        hits = form.cleaned_data.get("hits")
        assignee = form.cleaned_data.get("assignee")
        hits.update(assignee=assignee)
        messages.add_message(self.request, messages.SUCCESS, "Successfully assignment")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "An error has occurred")
        return super().form_invalid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        if user.id != 1:
            subordinates = user.subordinates.all()
            assignee_queryset = form.fields["assigned"].queryset
            form.fields["assigned"].queryset = assignee_queryset.filter(
                id__in=subordinates
            )
            hits_queryset = form.fields["hits"].queryset
            form.fields["hits"].queryset = hits_queryset.filter(
                Q(assigned=user) | Q(assigned__in=subordinates)
            )
        return form

    def has_permission(self):
        user = self.request.user
        return user.id == 1 or user.subordinates.all()
