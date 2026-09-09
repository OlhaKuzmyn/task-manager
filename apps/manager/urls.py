from django.urls import path

from apps.manager.views import index

app_name = "manager"

urlpatterns = [
    path("", index, name="index"),
]
