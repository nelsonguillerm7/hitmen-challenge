"""Auth models."""

# Django
from django.contrib.auth.views import (
    LogoutView,
    LoginView,
)
from django.urls import path

# Views
from apps.users.views import (
    SignUpView,
    HitmanListView,
    HitmanDetailView,
    HitmanAddManagerCreateView,
)

app_name = "auth"

urlpatterns = (
    path(
        route="",
        view=LoginView.as_view(
            template_name="users/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        route="logout/",
        view=LogoutView.as_view(),
        name="logout",
    ),
    path(
        route="register/",
        view=SignUpView.as_view(),
        name="register",
    ),
    path(
        route="hitmen/",
        view=HitmanListView.as_view(),
        name="hitman_list",
    ),
    path(
        route="hitmen/<int:pk>/",
        view=HitmanDetailView.as_view(),
        name="hitman_detail",
    ),
    path(
        route="hitmen/add/managers/",
        view=HitmanAddManagerCreateView.as_view(),
        name="hitman_add_managers",
    ),
)
