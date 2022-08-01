# Django
from django.urls import path

# Views
from apps.hits.views import (
    HitListView,
    HitDetailView,
    HitCreateView,
    HitUpdateView,
    HitBulkUpdateView,
)

app_name = "hits"

urlpatterns = (
    path(
        route="hits/",
        view=HitListView.as_view(),
        name="hit_list",
    ),
    path(
        route="hits/<int:pk>/",
        view=HitDetailView.as_view(),
        name="hit_detail",
    ),
    path(
        route="hits/<int:pk>/update/",
        view=HitUpdateView.as_view(),
        name="hit_update",
    ),
    path(
        route="hits/create/",
        view=HitCreateView.as_view(),
        name="hit_create",
    ),
    path(
        route="hits/bulk/",
        view=HitBulkUpdateView.as_view(),
        name="hit_bulk",
    ),
)
