from django.urls import path

from apps.worker.views import (
    WorkerListView,
    WorkerCreateView,
    WorkerDetailView,
    WorkerUpdateView,
    WorkerDeleteView,
)

app_name = "worker"

urlpatterns = [
    path("", WorkerListView.as_view(), name="worker-list"),
    path("create", WorkerCreateView.as_view(), name="worker-create"),
    path("<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("update/<int:pk>/", WorkerUpdateView.as_view(), name="worker-update"),
    path("delete/<int:pk>/", WorkerDeleteView.as_view(), name="worker-delete"),
]
