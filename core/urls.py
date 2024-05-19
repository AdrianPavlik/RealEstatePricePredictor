# -*- encoding: utf-8 -*-


from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin route
    path("__reload__/", include("django_browser_reload.urls")),
    path("", include("apps.home.urls"))
]
