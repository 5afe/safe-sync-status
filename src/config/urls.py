from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    re_path("^$", include("blocks.urls")),
    path("admin/", admin.site.urls),
]
