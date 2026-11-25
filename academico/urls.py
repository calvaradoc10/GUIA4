
from django.urls import path
from .views import (
    EstudianteListView,
    EstudianteCreateView,
    EstudianteUpdateView,
    EstudianteDeleteView,
    CarreraListView,
    CarreraCreateView,
    CarreraUpdateView,
    CarreraDeleteView,    
    UniversidadListView,
    UniversidadCreateView,
    UniversidadUpdateView,
    UniversidadDeleteView,
    FacultadListView,
    FacultadCreateView,
    FacultadUpdateView,
    FacultadDeleteView,
    SemestreListView,
    SemestreCreateView,
    SemestreUpdateView,
    SemestreDeleteView,    
    PeriodoListView,
    PeriodoCreateView,
    PeriodoUpdateView,
    PeriodoDeleteView,
    CursoListView,
    CursoCreateView,
    CursoUpdateView,
    CursoDeleteView,
    ProfesorListView,
    ProfesorCreateView,
    ProfesorUpdateView,
    ProfesorDeleteView,
    SeccionListView,
    SeccionCreateView,
    SeccionUpdateView,
    SeccionDeleteView,
    MatriculaListView,
    MatriculaCreateView,
    MatriculaUpdateView,
    MatriculaDeleteView,
    NotaListView,
    NotaCreateView,
    NotaUpdateView,
    NotaDeleteView,

)

app_name = "academico"

urlpatterns = [

    # Listado de estudiantes
    path(
        "estudiantes/",
        EstudianteListView.as_view(),
        name="estudiante_lista"
    ),

    # Registrar estudiante
    path(
        "estudiantes/nuevo/",
        EstudianteCreateView.as_view(),
        name="estudiante_crear"
    ),

    # Editar estudiante
    path(
        "estudiantes/<int:pk>/editar/",
        EstudianteUpdateView.as_view(),
        name="estudiante_editar"
    ),

    # Eliminar estudiante
    path(
        "estudiantes/<int:pk>/eliminar/",
        EstudianteDeleteView.as_view(),
        name="estudiante_eliminar"
    ),




     
    # RUTAS DEL CRUD DE CARRERAS
    # ==========================================

    # Listado de carreras
    path(
        "carreras/",
        CarreraListView.as_view(),
        name="carrera_lista"
    ),

    # Registrar carrera
    path(
        "carreras/nueva/",
        CarreraCreateView.as_view(),
        name="carrera_crear"
    ),

    # Editar carrera
    path(
        "carreras/<int:pk>/editar/",
        CarreraUpdateView.as_view(),
        name="carrera_editar"
    ),

    # Eliminar carrera
    path(
        "carreras/<int:pk>/eliminar/",
        CarreraDeleteView.as_view(),
        name="carrera_eliminar"
    ),
    
    
    # ==========================================
    # RUTAS DEL CRUD DE UNIVERSIDADES
    # ==========================================

    # Listado de universidades
    path(
        "universidades/",
        UniversidadListView.as_view(),
        name="universidad_lista"
    ),

    # Registrar universidad
    path(
        "universidades/nueva/",
        UniversidadCreateView.as_view(),
        name="universidad_crear"
    ),

    # Editar universidad
    path(
        "universidades/<int:pk>/editar/",
        UniversidadUpdateView.as_view(),
        name="universidad_editar"
    ),

    # Eliminar universidad
    path(
        "universidades/<int:pk>/eliminar/",
        UniversidadDeleteView.as_view(),
        name="universidad_eliminar"
    ),
    
    # ==========================================
    # RUTAS DEL CRUD DE FACULTADES
    # ==========================================

    # Listado de facultades
    path(
        "facultades/",
        FacultadListView.as_view(),
        name="facultad_lista"
    ),

    # Registrar facultad
    path(
        "facultades/nueva/",
        FacultadCreateView.as_view(),
        name="facultad_crear"
    ),

    # Editar facultad
    path(
        "facultades/<int:pk>/editar/",
        FacultadUpdateView.as_view(),
        name="facultad_editar"
    ),

    # Eliminar facultad
    path(
        "facultades/<int:pk>/eliminar/",
        FacultadDeleteView.as_view(),
        name="facultad_eliminar"
    ),
    
    
    # ==========================================
    # RUTAS DEL CRUD DE SEMESTRES
    # ==========================================

    # Listado de semestres
    path(
        "semestres/",
        SemestreListView.as_view(),
        name="semestre_lista"
    ),

    # Registrar semestre
    path(
        "semestres/nuevo/",
        SemestreCreateView.as_view(),
        name="semestre_crear"
    ),

    # Editar semestre
    path(
        "semestres/<int:pk>/editar/",
        SemestreUpdateView.as_view(),
        name="semestre_editar"
    ),

    # Eliminar semestre
    path(
        "semestres/<int:pk>/eliminar/",
        SemestreDeleteView.as_view(),
        name="semestre_eliminar"
    ),
    
    # ==========================================
    # RUTAS DEL CRUD DE PERIODOS ACADEMICOS
    # ==========================================

    # Listado de periodos
    path(
        "periodos/",
        PeriodoListView.as_view(),
        name="periodo_lista"
    ),

    # Registrar periodo
    path(
        "periodos/nuevo/",
        PeriodoCreateView.as_view(),
        name="periodo_crear"
    ),

    # Editar periodo
    path(
        "periodos/<int:pk>/editar/",
        PeriodoUpdateView.as_view(),
        name="periodo_editar"
    ),

    # Eliminar periodo
    path(
        "periodos/<int:pk>/eliminar/",
        PeriodoDeleteView.as_view(),
        name="periodo_eliminar"
    ),
    
    
    # ==========================================
    # RUTAS DEL CRUD DE CURSOS
    # ==========================================

    # Listado de cursos
    path(
        "cursos/",
        CursoListView.as_view(),
        name="curso_lista"
    ),

    # Registrar curso
    path(
        "cursos/nuevo/",
        CursoCreateView.as_view(),
        name="curso_crear"
    ),

    # Editar curso
    path(
        "cursos/<int:pk>/editar/",
        CursoUpdateView.as_view(),
        name="curso_editar"
    ),

    # Eliminar curso
    path(
        "cursos/<int:pk>/eliminar/",
        CursoDeleteView.as_view(),
        name="curso_eliminar"
    ),
    
    
    # ==========================================
    # RUTAS DEL CRUD DE PROFESORES
    # ==========================================

    # Listado de profesores
    path(
        "profesores/",
        ProfesorListView.as_view(),
        name="profesor_lista"
    ),

    # Registrar profesor
    path(
        "profesores/nuevo/",
        ProfesorCreateView.as_view(),
        name="profesor_crear"
    ),

    # Editar profesor
    path(
        "profesores/<int:pk>/editar/",
        ProfesorUpdateView.as_view(),
        name="profesor_editar"
    ),

    # Eliminar profesor
    path(
        "profesores/<int:pk>/eliminar/",
        ProfesorDeleteView.as_view(),
        name="profesor_eliminar"
    ),

    # ==========================================
    # RUTAS DEL CRUD DE SECCIONES
    # ==========================================

    # Listado de secciones
    path(
        "secciones/",
        SeccionListView.as_view(),
        name="seccion_lista"
    ),

    # Registrar sección
    path(
        "secciones/nueva/",
        SeccionCreateView.as_view(),
        name="seccion_crear"
    ),

    # Editar sección
    path(
        "secciones/<int:pk>/editar/",
        SeccionUpdateView.as_view(),
        name="seccion_editar"
    ),

    # Eliminar sección
    path(
        "secciones/<int:pk>/eliminar/",
        SeccionDeleteView.as_view(),
        name="seccion_eliminar"
    ),
    
    # ==========================================
    # RUTAS DEL CRUD DE MATRICULAS
    # ==========================================

    # Listado de matrículas
    path(
        "matriculas/",
        MatriculaListView.as_view(),
        name="matricula_lista"
    ),

    # Registrar matrícula
    path(
        "matriculas/nueva/",
        MatriculaCreateView.as_view(),
        name="matricula_crear"
    ),

    # Editar matrícula
    path(
        "matriculas/<int:pk>/editar/",
        MatriculaUpdateView.as_view(),
        name="matricula_editar"
    ),

    # Eliminar matrícula
    path(
        "matriculas/<int:pk>/eliminar/",
        MatriculaDeleteView.as_view(),
        name="matricula_eliminar"
    ),
    
    # ==========================================
    # RUTAS DEL CRUD DE NOTAS
    # ==========================================

    # Listado de notas
    path(
        "notas/",
        NotaListView.as_view(),
        name="nota_lista"
    ),

    # Registrar calificaciones
    path(
        "notas/nueva/",
        NotaCreateView.as_view(),
        name="nota_crear"
    ),

    # Editar calificaciones
    path(
        "notas/<int:pk>/editar/",
        NotaUpdateView.as_view(),
        name="nota_editar"
    ),

    # Eliminar registro de notas
    path(
        "notas/<int:pk>/eliminar/",
        NotaDeleteView.as_view(),
        name="nota_eliminar"
    ),
    
]