from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from core import settings
from django.conf.urls.static import static
from django.urls import re_path
urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("auth/", include("authentication.urls")),
        path("", include("application.urls")),
        path("__reload__/", include("django_browser_reload.urls")),
        path("select2/", include("django_select2.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r"^rosetta/", include("rosetta.urls")),
    ] 