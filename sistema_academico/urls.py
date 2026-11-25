"""Rutas principales del Sistema Académico."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from core.views import AccesoView, InicioView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", AccesoView.as_view(), name="login"),
    # LogoutView acepta POST; se incluye CSRF en todos los formularios de salida.
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("academico/", include("academico.urls")),
    path("", InicioView.as_view(), name="inicio"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
