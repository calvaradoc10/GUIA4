from django.shortcuts import redirect
from django.db.models.deletion import ProtectedError
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from core.mixins import FiltroCamposMixin
from .models import Estudiante, Carrera,Universidad,Facultad,Semestre,Periodo,Curso,Profesor,Seccion,Matricula,Nota
from .forms import EstudianteForm, CarreraForm,UniversidadForm,FacultadForm,SemestreForm,PeriodoForm,CursoForm,ProfesorForm,SeccionForm,MatriculaForm,NotaForm
from django.contrib import messages


class EstudianteListView(LoginRequiredMixin, FiltroCamposMixin, ListView):
    model = Estudiante
    template_name = "academico/estudiante_lista.html"
    context_object_name = "estudiantes"
    paginate_by = 10

    # Título que utilizaremos en el reporte PDF
    titulo_reporte = "Reporte de Estudiantes"

    # Columnas disponibles
    campos_disponibles = {
        "cedula": "Cédula",
        "nombres": "Nombres",
        "apellidos": "Apellidos",
        "carrera__nombre": "Carrera",
    }

    # Columnas que aparecerán inicialmente
    campos_por_defecto = [
        "cedula",
        "nombres",
        "apellidos",
        "carrera__nombre",
    ]

    # Ordenar los estudiantes alfabéticamente
    ordering = ["apellidos", "nombres"]



    def get_queryset(self):
        queryset = super().get_queryset()

        # Buscar por nombre, apellido, cédula o carrera
        busqueda = self.request.GET.get("buscar", "").strip()


        if busqueda:
            condiciones = Q()

            condiciones.add(
                Q(cedula__icontains=busqueda), Q.OR
            )
            condiciones.add(
                Q(nombres__icontains=busqueda), Q.OR
            )
            condiciones.add(
                Q(apellidos__icontains=busqueda), Q.OR
            )
            condiciones.add(
                Q(carrera__nombre__icontains=busqueda), Q.OR
            )

            queryset = queryset.filter(condiciones)


        # Filtrar por la carrera seleccionada
        carrera_id = self.request.GET.get("carrera", "").strip()

        if carrera_id.isdigit():
            queryset = queryset.filter(
                carrera_id=int(carrera_id)
            )

        return queryset

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        # Mostrar las carreras disponibles
        contexto["carreras"] = Carrera.objects.order_by("nombre")

        # Conservar la carrera seleccionada
        contexto["carrera_seleccionada"] = (
            self.request.GET.get("carrera", "")
        )

        # Relacionar cada estudiante con su fila
        contexto["filas_con_estudiante"] = list(
            zip(contexto["object_list"], contexto["filas"])
        )

        return contexto




# ==========================================
# REGISTRAR ESTUDIANTE
# ==========================================

class EstudianteCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    model = Estudiante
    form_class = EstudianteForm
    template_name = "academico/estudiante_form.html"
    success_url = reverse_lazy("academico:estudiante_lista")
    success_message = "Estudiante registrado correctamente."
    login_url = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# ==========================================
# EDITAR ESTUDIANTE
# ==========================================

class EstudianteUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Estudiante
    form_class = EstudianteForm
    template_name = "academico/estudiante_form.html"
    success_url = reverse_lazy("academico:estudiante_lista")
    success_message = "Estudiante actualizado correctamente."
    login_url = "login"



# ==========================================
# ELIMINAR ESTUDIANTE
# ==========================================

class EstudianteDeleteView(
    LoginRequiredMixin,
    DeleteView
):
    model = Estudiante
    template_name = "academico/estudiante_confirmar_eliminar.html"
    success_url = reverse_lazy("academico:estudiante_lista")
    login_url = "login"

    def form_valid(self, form):
        try:
            respuesta = super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                "No se puede eliminar este estudiante porque tiene matrículas relacionadas."
            )
            return redirect("academico:estudiante_lista")

        messages.success(self.request, "Estudiante eliminado correctamente.")
        return respuesta


# ==========================================
# LISTADO DE CARRERAS
# ==========================================

class CarreraListView(
    LoginRequiredMixin,
    FiltroCamposMixin,
    ListView
):
    model = Carrera
    template_name = "academico/carrera_lista.html"
    context_object_name = "carreras"
    paginate_by = 10
    login_url = "login"

    titulo_reporte = "Reporte de Carreras"

    campos_disponibles = {
        "codigo": "Código",
        "nombre": "Carrera",
        "facultad__nombre": "Facultad",
        "duracion_semestres": "Semestres",
    }

    campos_por_defecto = [
        "codigo",
        "nombre",
        "facultad__nombre",
        "duracion_semestres",
    ]

    ordering = ["nombre"]

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.select_related(
            "facultad",
            "facultad__universidad"
        )

        busqueda = self.request.GET.get(
            "buscar", ""
        ).strip()

        if busqueda:
            condiciones = Q()

            condiciones.add(
                Q(codigo__icontains=busqueda),
                Q.OR
            )

            condiciones.add(
                Q(nombre__icontains=busqueda),
                Q.OR
            )

            condiciones.add(
                Q(facultad__nombre__icontains=busqueda),
                Q.OR
            )

            queryset = queryset.filter(condiciones)

        return queryset

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        contexto["filas_con_carrera"] = list(
            zip(
                contexto["object_list"],
                contexto["filas"]
            )
        )

        return contexto


# ==========================================
# REGISTRAR CARRERA
# ==========================================

class CarreraCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    model = Carrera
    form_class = CarreraForm
    template_name = "academico/carrera_form.html"
    success_url = reverse_lazy("academico:carrera_lista")
    success_message = "Carrera registrada correctamente."
    login_url = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# ==========================================
# EDITAR CARRERA
# ==========================================

class CarreraUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Carrera
    form_class = CarreraForm
    template_name = "academico/carrera_form.html"
    success_url = reverse_lazy("academico:carrera_lista")
    success_message = "Carrera actualizada correctamente."
    login_url = "login"


# ==========================================
# ELIMINAR CARRERA
# ==========================================

class CarreraDeleteView(
    LoginRequiredMixin,
    DeleteView
):
    model = Carrera
    template_name = "academico/carrera_confirmar_eliminar.html"
    success_url = reverse_lazy("academico:carrera_lista")
    login_url = "login"

    def form_valid(self, form):
        try:
            respuesta = super().form_valid(form)

        except ProtectedError:
            messages.error(
                self.request,
                "No se puede eliminar esta carrera porque "
                "tiene estudiantes o cursos relacionados."
            )

            return redirect("academico:carrera_lista")

        messages.success(
            self.request,
            "Carrera eliminada correctamente."
        )

        return respuesta
    

# ==========================================
# LISTADO DE UNIVERSIDADES
# ==========================================

class UniversidadListView(
    LoginRequiredMixin,
    FiltroCamposMixin,
    ListView
):
    model = Universidad
    template_name = "academico/universidad_lista.html"
    context_object_name = "universidades"
    paginate_by = 10
    login_url = "login"

    titulo_reporte = "Reporte de Universidades"

    campos_disponibles = {
        "nombre": "Universidad",
        "siglas": "Siglas",
        "ciudad": "Ciudad",
    }

    campos_por_defecto = [
        "nombre",
        "siglas",
        "ciudad",
    ]

    ordering = ["nombre"]

    def get_queryset(self):
        queryset = super().get_queryset()

        busqueda = self.request.GET.get(
            "buscar", ""
        ).strip()

        if busqueda:
            queryset = queryset.filter(
                Q(nombre__icontains=busqueda) |
                Q(siglas__icontains=busqueda) |
                Q(ciudad__icontains=busqueda)
            )

        return queryset

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        contexto["filas_con_universidad"] = list(
            zip(
                contexto["object_list"],
                contexto["filas"]
            )
        )

        return contexto


# ==========================================
# REGISTRAR UNIVERSIDAD
# ==========================================

class UniversidadCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    model = Universidad
    form_class = UniversidadForm
    template_name = "academico/universidad_form.html"
    success_url = reverse_lazy("academico:universidad_lista")
    success_message = "Universidad registrada correctamente."
    login_url = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# ==========================================
# EDITAR UNIVERSIDAD
# ==========================================

class UniversidadUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Universidad
    form_class = UniversidadForm
    template_name = "academico/universidad_form.html"
    success_url = reverse_lazy("academico:universidad_lista")
    success_message = "Universidad actualizada correctamente."
    login_url = "login"


# ==========================================
# ELIMINAR UNIVERSIDAD
# ==========================================

class UniversidadDeleteView(
    LoginRequiredMixin,
    DeleteView
):
    model = Universidad
    template_name = "academico/universidad_confirmar_eliminar.html"
    success_url = reverse_lazy("academico:universidad_lista")
    login_url = "login"

    def form_valid(self, form):
        try:
            respuesta = super().form_valid(form)

        except ProtectedError:
            messages.error(
                self.request,
                "No se puede eliminar esta universidad "
                "porque tiene facultades relacionadas."
            )

            return redirect("academico:universidad_lista")

        messages.success(
            self.request,
            "Universidad eliminada correctamente."
        )

        return respuesta


# ==========================================
# LISTADO DE FACULTADES
# ==========================================

class FacultadListView(
    LoginRequiredMixin,
    FiltroCamposMixin,
    ListView
):
    model = Facultad
    template_name = "academico/facultad_lista.html"
    context_object_name = "facultades"
    paginate_by = 10
    login_url = "login"

    titulo_reporte = "Reporte de Facultades"

    # Columnas disponibles
    campos_disponibles = {
        "universidad__nombre": "Universidad",
        "nombre": "Facultad",
        "decano": "Decano",
    }

    # Columnas iniciales
    campos_por_defecto = [
        "universidad__nombre",
        "nombre",
        "decano",
    ]

    ordering = ["nombre"]

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.select_related(
            "universidad"
        )

        busqueda = self.request.GET.get(
            "buscar", ""
        ).strip()

        if busqueda:
            queryset = queryset.filter(
                Q(nombre__icontains=busqueda) |
                Q(universidad__nombre__icontains=busqueda) |
                Q(decano__icontains=busqueda)
            )

        return queryset

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        contexto["filas_con_facultad"] = list(
            zip(
                contexto["object_list"],
                contexto["filas"]
            )
        )

        return contexto


# ==========================================
# REGISTRAR FACULTAD
# ==========================================

class FacultadCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    model = Facultad
    form_class = FacultadForm
    template_name = "academico/facultad_form.html"
    success_url = reverse_lazy("academico:facultad_lista")
    success_message = "Facultad registrada correctamente."
    login_url = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# ==========================================
# EDITAR FACULTAD
# ==========================================

class FacultadUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Facultad
    form_class = FacultadForm
    template_name = "academico/facultad_form.html"
    success_url = reverse_lazy("academico:facultad_lista")
    success_message = "Facultad actualizada correctamente."
    login_url = "login"


# ==========================================
# ELIMINAR FACULTAD
# ==========================================

class FacultadDeleteView(
    LoginRequiredMixin,
    DeleteView
):
    model = Facultad
    template_name = "academico/facultad_confirmar_eliminar.html"
    success_url = reverse_lazy("academico:facultad_lista")
    login_url = "login"

    def form_valid(self, form):
        try:
            respuesta = super().form_valid(form)

        except ProtectedError:
            messages.error(
                self.request,
                "No se puede eliminar esta facultad "
                "porque tiene carreras relacionadas."
            )

            return redirect("academico:facultad_lista")

        messages.success(
            self.request,
            "Facultad eliminada correctamente."
        )

        return respuesta


# ==========================================
# LISTADO DE SEMESTRES
# ==========================================

class SemestreListView(
    LoginRequiredMixin,
    FiltroCamposMixin,
    ListView
):
    model = Semestre
    template_name = "academico/semestre_lista.html"
    context_object_name = "semestres"
    paginate_by = 10
    login_url = "login"

    titulo_reporte = "Reporte de Semestres"

    campos_disponibles = {
        "numero": "Número",
        "nombre": "Semestre",
    }

    campos_por_defecto = [
        "numero",
        "nombre",
    ]

    ordering = ["numero"]

    def get_queryset(self):
        queryset = super().get_queryset()

        busqueda = self.request.GET.get(
            "buscar", ""
        ).strip()

        if busqueda:
            filtros = Q(nombre__icontains=busqueda)

            if busqueda.isdigit():
                filtros |= Q(numero=int(busqueda))

            queryset = queryset.filter(filtros)

        return queryset

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        contexto["filas_con_semestre"] = list(
            zip(
                contexto["object_list"],
                contexto["filas"]
            )
        )

        return contexto


# ==========================================
# REGISTRAR SEMESTRE
# ==========================================

class SemestreCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    model = Semestre
    form_class = SemestreForm
    template_name = "academico/semestre_form.html"
    success_url = reverse_lazy(
        "academico:semestre_lista"
    )
    success_message = "Semestre registrado correctamente."
    login_url = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# ==========================================
# EDITAR SEMESTRE
# ==========================================

class SemestreUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Semestre
    form_class = SemestreForm
    template_name = "academico/semestre_form.html"
    success_url = reverse_lazy(
        "academico:semestre_lista"
    )
    success_message = "Semestre actualizado correctamente."
    login_url = "login"


# ==========================================
# ELIMINAR SEMESTRE
# ==========================================

class SemestreDeleteView(
    LoginRequiredMixin,
    DeleteView
):
    model = Semestre
    template_name = "academico/semestre_confirmar_eliminar.html"
    success_url = reverse_lazy(
        "academico:semestre_lista"
    )
    login_url = "login"

    def form_valid(self, form):
        try:
            respuesta = super().form_valid(form)

        except ProtectedError:
            messages.error(
                self.request,
                "No se puede eliminar este semestre "
                "porque tiene registros académicos relacionados."
            )

            return redirect(
                "academico:semestre_lista"
            )

        messages.success(
            self.request,
            "Semestre eliminado correctamente."
        )

        return respuesta

# ==========================================
# LISTADO DE PERIODOS ACADEMICOS
# ==========================================

class PeriodoListView(
    LoginRequiredMixin,
    FiltroCamposMixin,
    ListView
):
    model = Periodo
    template_name = "academico/periodo_lista.html"
    context_object_name = "periodos"
    paginate_by = 10
    login_url = "login"

    titulo_reporte = "Reporte de Períodos Académicos"

    # Columnas disponibles
    campos_disponibles = {
        "nombre": "Período académico",
        "fecha_inicio": "Fecha de inicio",
        "fecha_fin": "Fecha de finalización",
        "activo": "Activo",
    }

    # Columnas que aparecen inicialmente
    campos_por_defecto = [
        "nombre",
        "fecha_inicio",
        "fecha_fin",
        "activo",
    ]

    # Mostrar primero los períodos más recientes
    ordering = ["-fecha_inicio"]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Buscar por nombre del período
        busqueda = self.request.GET.get(
            "buscar", ""
        ).strip()

        if busqueda:
            queryset = queryset.filter(
                Q(nombre__icontains=busqueda)
            )

        # Filtrar por estado
        estado = self.request.GET.get(
            "estado", ""
        ).strip()

        if estado == "activo":
            queryset = queryset.filter(activo=True)

        elif estado == "inactivo":
            queryset = queryset.filter(activo=False)

        return queryset

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        contexto["filas_con_periodo"] = list(
            zip(
                contexto["object_list"],
                contexto["filas"]
            )
        )

        contexto["estado_seleccionado"] = (
            self.request.GET.get("estado", "")
        )

        return contexto


# ==========================================
# REGISTRAR PERIODO ACADEMICO
# ==========================================

class PeriodoCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    model = Periodo
    form_class = PeriodoForm
    template_name = "academico/periodo_form.html"

    success_url = reverse_lazy(
        "academico:periodo_lista"
    )

    success_message = (
        "Período académico registrado correctamente."
    )

    login_url = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


# ==========================================
# EDITAR PERIODO ACADEMICO
# ==========================================

class PeriodoUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Periodo
    form_class = PeriodoForm
    template_name = "academico/periodo_form.html"

    success_url = reverse_lazy(
        "academico:periodo_lista"
    )

    success_message = (
        "Período académico actualizado correctamente."
    )

    login_url = "login"


# ==========================================
# ELIMINAR PERIODO ACADEMICO
# ==========================================

class PeriodoDeleteView(
    LoginRequiredMixin,
    DeleteView
):
    model = Periodo

    template_name = (
        "academico/periodo_confirmar_eliminar.html"
    )

    success_url = reverse_lazy(
        "academico:periodo_lista"
    )

    login_url = "login"

    def form_valid(self, form):

        try:
            respuesta = super().form_valid(form)

        except ProtectedError:

            messages.error(
                self.request,
                "No se puede eliminar este período académico "
                "porque tiene registros relacionados."
            )

            return redirect(
                "academico:periodo_lista"
            )

        messages.success(
            self.request,
            "Período académico eliminado correctamente."
        )

        return respuesta


# ==========================================
# LISTADO DE CURSOS
# ==========================================

class CursoListView(
    LoginRequiredMixin,
    FiltroCamposMixin,
    ListView
):
    model = Curso
    template_name = "academico/curso_lista.html"
    context_object_name = "cursos"
    paginate_by = 10
    login_url = "login"

    titulo_reporte = "Reporte de Cursos Académicos"

    # Columnas disponibles
    campos_disponibles = {
        "codigo": "Código",
        "nombre": "Asignatura",
        "carrera__nombre": "Carrera",
        "semestre__nombre": "Semestre",
        "creditos": "Créditos",
    }

    # Columnas iniciales
    campos_por_defecto = [
        "codigo",
        "nombre",
        "carrera__nombre",
        "semestre__nombre",
        "creditos",
    ]

    # Ordenar por carrera, semestre y nombre
    ordering = [
        "carrera__nombre",
        "semestre__numero",
        "nombre",
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.select_related(
            "carrera",
            "semestre",
        )

        # Buscar por código, asignatura o carrera
        busqueda = self.request.GET.get(
            "buscar", ""
        ).strip()

        if busqueda:
            queryset = queryset.filter(
                Q(codigo__icontains=busqueda) |
                Q(nombre__icontains=busqueda) |
                Q(carrera__nombre__icontains=busqueda) |
                Q(semestre__nombre__icontains=busqueda)
            )

        # Filtrar por carrera
        carrera_id = self.request.GET.get(
            "carrera", ""
        )

        if carrera_id.isdigit():
            queryset = queryset.filter(
                carrera_id=int(carrera_id)
            )

        # Filtrar por semestre
        semestre_id = self.request.GET.get(
            "semestre", ""
        )

        if semestre_id.isdigit():
            queryset = queryset.filter(
                semestre_id=int(semestre_id)
            )

        return queryset

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        # Asociar cada objeto con sus columnas
        contexto["filas_con_curso"] = list(
            zip(
                contexto["object_list"],
                contexto["filas"]
            )
        )

        # Opciones para los filtros
        contexto["carreras"] = Carrera.objects.all().order_by(
            "nombre"
        )

        contexto["semestres"] = Semestre.objects.all().order_by(
            "numero"
        )

        contexto["carrera_seleccionada"] = (
            self.request.GET.get("carrera", "")
        )

        contexto["semestre_seleccionado"] = (
            self.request.GET.get("semestre", "")
        )

        return contexto


# ==========================================
# REGISTRAR CURSO
# ==========================================

class CursoCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    model = Curso
    form_class = CursoForm
    template_name = "academico/curso_form.html"

    success_url = reverse_lazy(
        "academico:curso_lista"
    )

    success_message = (
        "Curso registrado correctamente."
    )

    login_url = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


# ==========================================
# EDITAR CURSO
# ==========================================

class CursoUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Curso
    form_class = CursoForm
    template_name = "academico/curso_form.html"

    success_url = reverse_lazy(
        "academico:curso_lista"
    )

    success_message = (
        "Curso actualizado correctamente."
    )

    login_url = "login"


# ==========================================
# ELIMINAR CURSO
# ==========================================

class CursoDeleteView(
    LoginRequiredMixin,
    DeleteView
):
    model = Curso

    template_name = (
        "academico/curso_confirmar_eliminar.html"
    )

    success_url = reverse_lazy(
        "academico:curso_lista"
    )

    login_url = "login"

    def form_valid(self, form):
        try:
            respuesta = super().form_valid(form)

        except ProtectedError:
            messages.error(
                self.request,
                "No se puede eliminar este curso "
                "porque tiene registros académicos relacionados."
            )

            return redirect(
                "academico:curso_lista"
            )

        messages.success(
            self.request,
            "Curso eliminado correctamente."
        )

        return respuesta


# ==========================================
# LISTADO DE PROFESORES
# ==========================================

class ProfesorListView(
    LoginRequiredMixin,
    FiltroCamposMixin,
    ListView
):
    model = Profesor
    template_name = "academico/profesor_lista.html"
    context_object_name = "profesores"
    paginate_by = 10
    login_url = "login"

    titulo_reporte = "Reporte de Profesores"

    # Columnas disponibles
    campos_disponibles = {
        "cedula": "Cédula",
        "nombres": "Nombres",
        "apellidos": "Apellidos",
        "email": "Correo electrónico",
        "titulo": "Título académico",
    }

    # Columnas que aparecen inicialmente
    campos_por_defecto = [
        "cedula",
        "nombres",
        "apellidos",
        "email",
        "titulo",
    ]

    # Ordenar alfabéticamente
    ordering = ["apellidos", "nombres"]

    def get_queryset(self):
        queryset = super().get_queryset()

        busqueda = self.request.GET.get(
            "buscar", ""
        ).strip()

        if busqueda:
            queryset = queryset.filter(
                Q(cedula__icontains=busqueda) |
                Q(nombres__icontains=busqueda) |
                Q(apellidos__icontains=busqueda) |
                Q(email__icontains=busqueda) |
                Q(titulo__icontains=busqueda)
            )

        return queryset

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        contexto["filas_con_profesor"] = list(
            zip(
                contexto["object_list"],
                contexto["filas"]
            )
        )

        return contexto


# ==========================================
# REGISTRAR PROFESOR
# ==========================================

class ProfesorCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    model = Profesor
    form_class = ProfesorForm
    template_name = "academico/profesor_form.html"

    success_url = reverse_lazy(
        "academico:profesor_lista"
    )

    success_message = (
        "Profesor registrado correctamente."
    )

    login_url = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


# ==========================================
# EDITAR PROFESOR
# ==========================================

class ProfesorUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Profesor
    form_class = ProfesorForm
    template_name = "academico/profesor_form.html"

    success_url = reverse_lazy(
        "academico:profesor_lista"
    )

    success_message = (
        "Profesor actualizado correctamente."
    )

    login_url = "login"


# ==========================================
# ELIMINAR PROFESOR
# ==========================================

class ProfesorDeleteView(
    LoginRequiredMixin,
    DeleteView
):
    model = Profesor

    template_name = (
        "academico/profesor_confirmar_eliminar.html"
    )

    success_url = reverse_lazy(
        "academico:profesor_lista"
    )

    login_url = "login"

    def form_valid(self, form):
        try:
            respuesta = super().form_valid(form)

        except ProtectedError:
            messages.error(
                self.request,
                "No se puede eliminar este profesor "
                "porque tiene registros académicos relacionados."
            )

            return redirect(
                "academico:profesor_lista"
            )

        messages.success(
            self.request,
            "Profesor eliminado correctamente."
        )

        return respuesta


# ==========================================
# LISTADO DE SECCIONES ACADEMICAS
# ==========================================

class SeccionListView(
    LoginRequiredMixin,
    FiltroCamposMixin,
    ListView
):
    model = Seccion
    template_name = "academico/seccion_lista.html"
    context_object_name = "secciones"
    paginate_by = 10
    login_url = "login"

    titulo_reporte = "Reporte de Secciones Académicas"

    # Columnas disponibles
    campos_disponibles = {
        "curso__codigo": "Código del curso",
        "curso__nombre": "Asignatura",
        "periodo__nombre": "Período",
        "profesor__nombres": "Nombres del profesor",
        "profesor__apellidos": "Apellidos del profesor",
        "paralelo": "Paralelo",
        "jornada": "Jornada",
        "cupo": "Cupo",
    }

    # Columnas mostradas inicialmente
    campos_por_defecto = [
        "curso__codigo",
        "curso__nombre",
        "periodo__nombre",
        "profesor__apellidos",
        "paralelo",
        "jornada",
        "cupo",
    ]

    ordering = [
        "curso__nombre",
        "periodo__nombre",
        "paralelo",
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Optimizar las relaciones
        queryset = queryset.select_related(
            "curso",
            "periodo",
            "profesor",
        )

        # ==================================
        # BUSCADOR GENERAL
        # ==================================

        busqueda = self.request.GET.get(
            "buscar", ""
        ).strip()

        if busqueda:
            queryset = queryset.filter(
                Q(curso__codigo__icontains=busqueda) |
                Q(curso__nombre__icontains=busqueda) |
                Q(periodo__nombre__icontains=busqueda) |
                Q(profesor__nombres__icontains=busqueda) |
                Q(profesor__apellidos__icontains=busqueda) |
                Q(paralelo__icontains=busqueda)
            )

        # ==================================
        # FILTRAR POR CURSO
        # ==================================

        curso_id = self.request.GET.get(
            "curso", ""
        )

        if curso_id.isdigit():
            queryset = queryset.filter(
                curso_id=int(curso_id)
            )

        # ==================================
        # FILTRAR POR PERIODO
        # ==================================

        periodo_id = self.request.GET.get(
            "periodo", ""
        )

        if periodo_id.isdigit():
            queryset = queryset.filter(
                periodo_id=int(periodo_id)
            )

        # ==================================
        # FILTRAR POR JORNADA
        # ==================================

        jornada = self.request.GET.get(
            "jornada", ""
        )

        jornadas_validas = [
            valor
            for valor, etiqueta in
            Seccion._meta.get_field("jornada").choices
        ]

        if jornada in jornadas_validas:
            queryset = queryset.filter(
                jornada=jornada
            )

        return queryset

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        # Relacionar objetos con filas
        contexto["filas_con_seccion"] = list(
            zip(
                contexto["object_list"],
                contexto["filas"]
            )
        )

        # Datos para los filtros
        contexto["cursos"] = Curso.objects.all().order_by(
            "nombre"
        )

        contexto["periodos"] = Periodo.objects.all().order_by(
            "-fecha_inicio"
        )

        contexto["jornadas"] = (
            Seccion._meta.get_field("jornada").choices
        )

        # Mantener los filtros seleccionados
        contexto["curso_seleccionado"] = (
            self.request.GET.get("curso", "")
        )

        contexto["periodo_seleccionado"] = (
            self.request.GET.get("periodo", "")
        )

        contexto["jornada_seleccionada"] = (
            self.request.GET.get("jornada", "")
        )

        return contexto


# ==========================================
# REGISTRAR SECCION ACADEMICA
# ==========================================

class SeccionCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    model = Seccion
    form_class = SeccionForm
    template_name = "academico/seccion_form.html"

    success_url = reverse_lazy(
        "academico:seccion_lista"
    )

    success_message = (
        "Sección académica registrada correctamente."
    )

    login_url = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


# ==========================================
# EDITAR SECCION ACADEMICA
# ==========================================

class SeccionUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Seccion
    form_class = SeccionForm
    template_name = "academico/seccion_form.html"

    success_url = reverse_lazy(
        "academico:seccion_lista"
    )

    success_message = (
        "Sección académica actualizada correctamente."
    )

    login_url = "login"


# ==========================================
# ELIMINAR SECCION ACADEMICA
# ==========================================

class SeccionDeleteView(
    LoginRequiredMixin,
    DeleteView
):
    model = Seccion

    template_name = (
        "academico/seccion_confirmar_eliminar.html"
    )

    success_url = reverse_lazy(
        "academico:seccion_lista"
    )

    login_url = "login"

    def form_valid(self, form):
        try:
            respuesta = super().form_valid(form)

        except ProtectedError:
            messages.error(
                self.request,
                "No se puede eliminar esta sección "
                "porque tiene matrículas o registros "
                "académicos relacionados."
            )

            return redirect(
                "academico:seccion_lista"
            )

        messages.success(
            self.request,
            "Sección académica eliminada correctamente."
        )

        return respuesta


# ==========================================
# LISTADO DE MATRICULAS ACADEMICAS
# ==========================================

class MatriculaListView(
    LoginRequiredMixin,
    FiltroCamposMixin,
    ListView
):
    model = Matricula
    template_name = "academico/matricula_lista.html"
    context_object_name = "matriculas"
    paginate_by = 10
    login_url = "login"

    titulo_reporte = "Reporte de Matrículas Académicas"

    # Columnas disponibles
    campos_disponibles = {
        "estudiante__cedula": "Cédula",
        "estudiante__nombres": "Nombres",
        "estudiante__apellidos": "Apellidos",
        "seccion__curso__codigo": "Código del curso",
        "seccion__curso__nombre": "Asignatura",
        "seccion__periodo__nombre": "Período",
        "seccion__paralelo": "Paralelo",
        "fecha": "Fecha de matrícula",
    }

    # Columnas iniciales
    campos_por_defecto = [
        "estudiante__cedula",
        "estudiante__nombres",
        "estudiante__apellidos",
        "seccion__curso__nombre",
        "seccion__periodo__nombre",
        "seccion__paralelo",
        "fecha",
    ]

    # Mostrar las matrículas más recientes
    ordering = [
        "-fecha",
        "estudiante__apellidos",
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Optimizar consultas relacionadas
        queryset = queryset.select_related(
            "estudiante",
            "seccion",
            "seccion__curso",
            "seccion__periodo",
        )

        # ======================================
        # BUSCADOR GENERAL
        # ======================================

        busqueda = self.request.GET.get(
            "buscar", ""
        ).strip()

        if busqueda:
            queryset = queryset.filter(
                Q(estudiante__cedula__icontains=busqueda) |
                Q(estudiante__nombres__icontains=busqueda) |
                Q(estudiante__apellidos__icontains=busqueda) |
                Q(seccion__curso__codigo__icontains=busqueda) |
                Q(seccion__curso__nombre__icontains=busqueda) |
                Q(seccion__periodo__nombre__icontains=busqueda)
            )

        # ======================================
        # FILTRO POR PERIODO ACADEMICO
        # ======================================

        periodo_id = self.request.GET.get(
            "periodo", ""
        ).strip()

        if periodo_id.isdigit():
            queryset = queryset.filter(
                seccion__periodo_id=int(periodo_id)
            )

        # ======================================
        # FILTRO POR SECCION
        # ======================================

        seccion_id = self.request.GET.get(
            "seccion", ""
        ).strip()

        if seccion_id.isdigit():
            queryset = queryset.filter(
                seccion_id=int(seccion_id)
            )

        return queryset

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        # Asociar matrículas con las filas de la tabla
        contexto["filas_con_matricula"] = list(
            zip(
                contexto["object_list"],
                contexto["filas"]
            )
        )

        # Opciones para filtros
        contexto["periodos"] = Periodo.objects.all().order_by(
            "-fecha_inicio"
        )

        contexto["secciones"] = (
            Seccion.objects.select_related(
                "curso",
                "periodo"
            ).order_by(
                "curso__nombre",
                "paralelo"
            )
        )

        # Mantener filtros seleccionados
        contexto["periodo_seleccionado"] = (
            self.request.GET.get("periodo", "")
        )

        contexto["seccion_seleccionada"] = (
            self.request.GET.get("seccion", "")
        )

        return contexto


# ==========================================
# REGISTRAR MATRICULA
# ==========================================

class MatriculaCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    model = Matricula
    form_class = MatriculaForm
    template_name = "academico/matricula_form.html"

    success_url = reverse_lazy(
        "academico:matricula_lista"
    )

    success_message = (
        "Matrícula académica registrada correctamente."
    )

    login_url = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# ==========================================
# EDITAR MATRICULA
# ==========================================

class MatriculaUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Matricula
    form_class = MatriculaForm
    template_name = "academico/matricula_form.html"

    success_url = reverse_lazy(
        "academico:matricula_lista"
    )

    success_message = (
        "Matrícula académica actualizada correctamente."
    )

    login_url = "login"


# ==========================================
# ELIMINAR MATRICULA
# ==========================================

class MatriculaDeleteView(
    LoginRequiredMixin,
    DeleteView
):
    model = Matricula

    template_name = (
        "academico/matricula_confirmar_eliminar.html"
    )

    success_url = reverse_lazy(
        "academico:matricula_lista"
    )

    login_url = "login"

    def form_valid(self, form):
        try:
            respuesta = super().form_valid(form)

        except ProtectedError:
            messages.error(
                self.request,
                "No se puede eliminar esta matrícula "
                "porque tiene notas u otros registros "
                "académicos relacionados."
            )

            return redirect(
                "academico:matricula_lista"
            )

        messages.success(
            self.request,
            "Matrícula académica eliminada correctamente."
        )

        return respuesta
    
    
# ==========================================
# LISTADO DE NOTAS ACADEMICAS
# ==========================================

class NotaListView(
    LoginRequiredMixin,
    FiltroCamposMixin,
    ListView
):
    model = Nota
    template_name = "academico/nota_lista.html"
    context_object_name = "notas"
    paginate_by = 10
    login_url = "login"

    titulo_reporte = "Reporte de Calificaciones Académicas"

    # Columnas disponibles
    campos_disponibles = {
        "matricula__estudiante__cedula": "Cédula",
        "matricula__estudiante__nombres": "Nombres",
        "matricula__estudiante__apellidos": "Apellidos",
        "matricula__seccion__curso__nombre": "Asignatura",
        "matricula__seccion__periodo__nombre": "Período",
        "n1": "Nota 1",
        "n2": "Nota 2",
        "n3": "Nota 3",
        "promedio": "Promedio",
        "estado": "Estado académico",
    }

    # Columnas iniciales
    campos_por_defecto = [
        "matricula__estudiante__cedula",
        "matricula__estudiante__nombres",
        "matricula__estudiante__apellidos",
        "matricula__seccion__curso__nombre",
        "n1",
        "n2",
        "n3",
        "promedio",
        "estado",
    ]

    ordering = [
        "matricula__estudiante__apellidos",
        "matricula__estudiante__nombres",
    ]

    # Mostrar el estado en español
    def obtener_valor_campo(self, objeto, campo):

        if campo == "estado":
            return objeto.get_estado_display()

        return super().obtener_valor_campo(
            objeto,
            campo
        )

    # ======================================
    # BUSQUEDAS Y FILTROS
    # ======================================

    def get_queryset(self):

        queryset = super().get_queryset()

        # Optimizar las relaciones
        queryset = queryset.select_related(
            "matricula",
            "matricula__estudiante",
            "matricula__seccion",
            "matricula__seccion__curso",
            "matricula__seccion__periodo",
        )

        # Buscar estudiante o asignatura
        busqueda = self.request.GET.get(
            "buscar", ""
        ).strip()

        if busqueda:

            queryset = queryset.filter(
                Q(
                    matricula__estudiante__cedula__icontains=busqueda
                )
                |
                Q(
                    matricula__estudiante__nombres__icontains=busqueda
                )
                |
                Q(
                    matricula__estudiante__apellidos__icontains=busqueda
                )
                |
                Q(
                    matricula__seccion__curso__codigo__icontains=busqueda
                )
                |
                Q(
                    matricula__seccion__curso__nombre__icontains=busqueda
                )
            )

        # ======================================
        # FILTRAR POR PERIODO
        # ======================================

        periodo_id = self.request.GET.get(
            "periodo", ""
        ).strip()

        if periodo_id.isdigit():

            queryset = queryset.filter(
                matricula__seccion__periodo_id=int(
                    periodo_id
                )
            )

        # ======================================
        # FILTRAR POR ESTADO
        # ======================================

        estado = self.request.GET.get(
            "estado", ""
        ).strip()

        if estado in ["aprobado", "reprobado"]:

            queryset = queryset.filter(
                estado=estado
            )

        return queryset

    # ======================================
    # DATOS PARA LA PLANTILLA
    # ======================================

    def get_context_data(self, **kwargs):

        contexto = super().get_context_data(
            **kwargs
        )

        # Relacionar notas con las filas de la tabla
        contexto["filas_con_nota"] = list(
            zip(
                contexto["object_list"],
                contexto["filas"]
            )
        )

        # Períodos disponibles
        contexto["periodos"] = (
            Periodo.objects.all().order_by(
                "-fecha_inicio"
            )
        )

        # Conservar período seleccionado
        contexto["periodo_seleccionado"] = (
            self.request.GET.get("periodo", "")
        )

        # Conservar estado seleccionado
        contexto["estado_seleccionado"] = (
            self.request.GET.get("estado", "")
        )

        return contexto


# ==========================================
# REGISTRAR NOTA ACADEMICA
# ==========================================

class NotaCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    model = Nota
    form_class = NotaForm

    template_name = "academico/nota_form.html"

    success_url = reverse_lazy(
        "academico:nota_lista"
    )

    success_message = (
        "Calificaciones registradas correctamente."
    )

    login_url = "login"

    def form_valid(self, form):

        form.instance.user = self.request.user

        return super().form_valid(form)


# ==========================================
# EDITAR NOTA ACADEMICA
# ==========================================

class NotaUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Nota
    form_class = NotaForm

    template_name = "academico/nota_form.html"

    success_url = reverse_lazy(
        "academico:nota_lista"
    )

    success_message = (
        "Calificaciones actualizadas correctamente."
    )

    login_url = "login"


# ==========================================
# ELIMINAR NOTA ACADEMICA
# ==========================================

class NotaDeleteView(
    LoginRequiredMixin,
    DeleteView
):
    model = Nota

    template_name = (
        "academico/nota_confirmar_eliminar.html"
    )

    success_url = reverse_lazy(
        "academico:nota_lista"
    )

    login_url = "login"

    def form_valid(self, form):

        respuesta = super().form_valid(form)

        messages.success(
            self.request,
            "Registro de calificaciones eliminado correctamente."
        )

        return respuesta


