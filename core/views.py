"""Vistas basadas en clases para el acceso y panel principal."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from academico.models import Estudiante, Curso, Matricula, Nota
from .forms import AccesoForm


class AccesoView(LoginView):
    template_name = "core/login.html"
    authentication_form = AccesoForm
    redirect_authenticated_user = True
    next_page = reverse_lazy("inicio")


class InicioView(LoginRequiredMixin, TemplateView):
    template_name = "academico/inicio.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto.update({
            "total_estudiantes": Estudiante.objects.count(),
            "total_cursos": Curso.objects.count(),
            "total_matriculas": Matricula.objects.count(),
            "total_notas": Nota.objects.count(),
        })
        return contexto
