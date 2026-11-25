
# academico/admin.py
# Configuración del panel administrativo

from django.contrib import admin

from .models import (
    Universidad, Facultad, Carrera, Semestre,
    Periodo, Curso, Profesor, Estudiante,
    Seccion, Matricula, Nota
)


# Clase administrativa reutilizable
class BaseAdmin(admin.ModelAdmin):

    # Campos visibles, pero no modificables
    readonly_fields = (
        "user",
        "fecha_creacion",
        "fecha_modificacion"
    )

    # Asignar automáticamente el usuario que guarda
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


# Administrador de universidades
@admin.register(Universidad)
class UniversidadAdmin(BaseAdmin):
    list_display = ("id", "nombre", "siglas", "ciudad")
    search_fields = ("nombre", "siglas", "ciudad")
    list_filter = ("ciudad",)


# Administrador de facultades
@admin.register(Facultad)
class FacultadAdmin(BaseAdmin):
    list_display = ("id", "nombre", "universidad", "decano")
    search_fields = ("nombre", "decano", "universidad__nombre")
    list_filter = ("universidad",)


# Administrador de carreras
@admin.register(Carrera)
class CarreraAdmin(BaseAdmin):
    list_display = (
        "id", "codigo", "nombre",
        "facultad", "duracion_semestres"
    )
    search_fields = ("codigo", "nombre", "facultad__nombre")
    list_filter = ("facultad",)



# Administrador de semestres
@admin.register(Semestre)
class SemestreAdmin(BaseAdmin):
    list_display = ("id", "numero", "nombre")
    search_fields = ("nombre",)
    list_filter = ("numero",)


# Administrador de periodos académicos
@admin.register(Periodo)
class PeriodoAdmin(BaseAdmin):
    list_display = (
        "id", "nombre", "fecha_inicio",
        "fecha_fin", "activo"
    )
    search_fields = ("nombre",)
    list_filter = ("activo", "fecha_inicio")


# Administrador de cursos
@admin.register(Curso)
class CursoAdmin(BaseAdmin):
    list_display = (
        "id", "codigo", "nombre",
        "carrera", "semestre", "creditos"
    )
    search_fields = (
        "codigo", "nombre", "carrera__nombre"
    )
    list_filter = ("carrera", "semestre")


# Administrador de profesores
@admin.register(Profesor)
class ProfesorAdmin(BaseAdmin):
    list_display = (
        "id", "cedula", "nombres",
        "apellidos", "email", "titulo"
    )

    search_fields = (
        "cedula", "nombres", "apellidos", "email"
    )

    list_filter = ("titulo",)


# Administrador de estudiantes
@admin.register(Estudiante)
class EstudianteAdmin(BaseAdmin):
    list_display = (
        "id", "cedula", "nombres",
        "apellidos", "carrera", "email"
    )

    search_fields = (
        "cedula", "nombres", "apellidos",
        "email", "carrera__nombre"
    )

    list_filter = ("carrera",)



# Administrador de secciones académicas
@admin.register(Seccion)
class SeccionAdmin(BaseAdmin):
    list_display = (
        "id", "curso", "periodo", "profesor",
        "paralelo", "jornada", "cupo", "inscritos"
    )

    search_fields = (
        "curso__nombre", "curso__codigo",
        "profesor__nombres", "profesor__apellidos"
    )

    list_filter = ("periodo", "jornada", "curso")


# Permite registrar notas dentro de una matrícula
class NotaInline(admin.StackedInline):
    model = Nota
    max_num = 1
    extra = 1


# Administrador de matrículas
@admin.register(Matricula)
class MatriculaAdmin(BaseAdmin):
    list_display = (
        "id", "estudiante", "seccion", "fecha"
    )

    search_fields = (
        "estudiante__cedula",
        "estudiante__nombres",
        "estudiante__apellidos",
        "seccion__curso__nombre"
    )

    list_filter = (
        "seccion__periodo",
        "seccion__jornada",
        "fecha"
    )

    # Mostrar las notas dentro de la matrícula
    inlines = [NotaInline]


# Administrador de notas
@admin.register(Nota)
class NotaAdmin(BaseAdmin):
    list_display = (
        "id", "matricula", "n1", "n2",
        "n3", "promedio", "estado"
    )

    search_fields = (
        "matricula__estudiante__cedula",
        "matricula__estudiante__nombres",
        "matricula__estudiante__apellidos"
    )

    list_filter = ("estado",)
