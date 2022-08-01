from django.urls import path

from apps.flows.views import ChangeStateView

app_name = "flows"

urlpatterns = [
    path(
        route="change/state/<slug:app>/<slug:model>/<slug:transition>/<int:pk>/",
        view=ChangeStateView.as_view(),
        name="workflow_transition",
    ),
]
