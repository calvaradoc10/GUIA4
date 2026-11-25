
# academico/models.py
# Modelos del Sistema Académico

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from core.models import ModeloBase

# Reglas de las calificaciones
NOTA_MINIMA_APROBACION = Decimal("70")
NOTA_MAXIMA = Decimal("100")
VALIDAR_NOTA = [
    MinValueValidator(Decimal("0")),
    MaxValueValidator(NOTA_MAXIMA)
]


# Opciones de jornada
class Jornada(models.TextChoices):
    DIURNA = "diurna", "Diurna"
    NOCTURNA = "nocturna", "Nocturna"


# Opciones de estado académico
class EstadoNota(models.TextChoices):
    APROBADO = "aprobado", "Aprobado"
    REPROBADO = "reprobado", "Reprobado"


# Modelo Universidad
class Universidad(ModeloBase):
    nombre = models.CharField(max_length=150, unique=True)
    siglas = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=80)
    logo = models.ImageField(
        upload_to="universidades/",
        blank=True
    )

    class Meta:
        verbose_name = "Universidad"
        verbose_name_plural = "Universidades"
        ordering = ["nombre"]

    def __str__(self):
        return self.siglas
    

# Modelo Facultad
class Facultad(ModeloBase):
    universidad = models.ForeignKey(
        Universidad,
        on_delete=models.PROTECT,
        related_name="facultades"
    )
    nombre = models.CharField(max_length=150)
    decano = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name = "Facultad"
        verbose_name_plural = "Facultades"
        ordering = ["nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["universidad", "nombre"],
                name="facultad_unica_por_universidad"
            ),
        ]

    def __str__(self):
        return self.nombre



# Modelo Carrera
class Carrera(ModeloBase):
    facultad = models.ForeignKey(
        Facultad,
        on_delete=models.PROTECT,
        related_name="carreras"
    )

    codigo = models.CharField(
        "Código",
        max_length=10,
        unique=True
    )

    nombre = models.CharField(max_length=150)

    duracion_semestres = models.PositiveSmallIntegerField(
        "Duración (semestres)",
        default=8
    )

    class Meta:
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre



# Modelo Semestre
class Semestre(ModeloBase):
    numero = models.PositiveSmallIntegerField(
        unique=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12)
        ]
    )

    nombre = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Semestre"
        verbose_name_plural = "Semestres"
        ordering = ["numero"]

    def __str__(self):
        return self.nombre



# Modelo Periodo
class Periodo(ModeloBase):
    nombre = models.CharField(max_length=20, unique=True)

    fecha_inicio = models.DateField("Fecha de inicio")
    fecha_fin = models.DateField("Fecha de fin")

    activo = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Periodo"
        verbose_name_plural = "Periodos"
        ordering = ["-fecha_inicio"]

    def __str__(self):
        return self.nombre

    def clean(self):
        # Verifica que la fecha final sea posterior a la inicial
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin <= self.fecha_inicio:
            raise ValidationError({
                "fecha_fin": "La fecha de fin debe ser posterior a la de inicio."
            })


# Modelo Curso: representa una materia de una carrera
class Curso(ModeloBase):
    # Carrera a la que pertenece la materia
    carrera = models.ForeignKey(
        Carrera,
        on_delete=models.PROTECT,
        related_name="cursos"
    )

    # Semestre en el que se imparte
    semestre = models.ForeignKey(
        Semestre,
        on_delete=models.PROTECT,
        related_name="cursos"
    )

    # Información del curso
    codigo = models.CharField("Código", max_length=12, unique=True)
    nombre = models.CharField(max_length=150)
    creditos = models.PositiveSmallIntegerField("Créditos", default=3)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["carrera", "semestre__numero", "nombre"]

    def __str__(self):
        return f"{self.codigo} · {self.nombre}"


# Modelo Profesor
class Profesor(ModeloBase):
    cedula = models.CharField(
        "Cédula",
        max_length=10,
        unique=True
    )

    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)

    email = models.EmailField(
        "Correo",
        blank=True
    )

    titulo = models.CharField(
        "Título",
        max_length=120,
        blank=True
    )

    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"
        ordering = ["apellidos", "nombres"]

    def __str__(self):
        return f"{self.apellidos} {self.nombres}"


# Modelo Estudiante
class Estudiante(ModeloBase):
    cedula = models.CharField(
        "Cédula",
        max_length=10,
        unique=True
    )

    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)

    email = models.EmailField(
        "Correo",
        blank=True
    )

    telefono = models.CharField(
        "Teléfono",
        max_length=15,
        blank=True
    )

    fecha_nacimiento = models.DateField(
        "Fecha de nacimiento",
        null=True,
        blank=True
    )

    # Relación del estudiante con una carrera
    carrera = models.ForeignKey(
        Carrera,
        on_delete=models.PROTECT,
        related_name="estudiantes"
    )

    # Fotografía opcional del estudiante
    foto = models.ImageField(
        upload_to="estudiantes/",
        blank=True
    )

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ["apellidos", "nombres"]

    def __str__(self):
        return f"{self.apellidos} {self.nombres}"

    def clean(self):
        super().clean()
        if self.pk and self.carrera_id and self.matriculas.exclude(
            seccion__curso__carrera_id=self.carrera_id
        ).exists():
            raise ValidationError({
                "carrera": "No se puede cambiar la carrera mientras existan matrículas incompatibles."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"


# Modelo Seccion: materia ofertada en un periodo académico
class Seccion(ModeloBase):

    # Curso que se imparte
    curso = models.ForeignKey(
        Curso,
        on_delete=models.PROTECT,
        related_name="secciones"
    )

    # Periodo académico
    periodo = models.ForeignKey(
        Periodo,
        on_delete=models.PROTECT,
        related_name="secciones"
    )

    # Profesor encargado
    profesor = models.ForeignKey(
        Profesor,
        on_delete=models.PROTECT,
        related_name="secciones"
    )

    # Información de la sección
    paralelo = models.CharField(max_length=2, default="A")

    jornada = models.CharField(
        max_length=10,
        choices=Jornada.choices,
        default=Jornada.DIURNA
    )

    cupo = models.PositiveSmallIntegerField(default=30)

    # Relación de estudiantes mediante las matrículas
    estudiantes = models.ManyToManyField(
        "Estudiante",
        through="Matricula",
        related_name="secciones"
    )

    class Meta:
        verbose_name = "Sección"
        verbose_name_plural = "Secciones"
        ordering = ["periodo", "curso", "paralelo"]
        constraints = [
            models.UniqueConstraint(
                fields=["curso", "periodo", "paralelo", "jornada"],
                name="seccion_unica"
            ),
        ]

    def __str__(self):
        return f"{self.curso.codigo} {self.paralelo} · {self.get_jornada_display()} · {self.periodo}"

    def clean(self):
        super().clean()
        if self.cupo is not None and self.cupo < 1:
            raise ValidationError({"cupo": "El cupo debe ser mayor que cero."})
        if self.pk:
            inscritos = self.matriculas.count()
            if self.cupo is not None and inscritos > self.cupo:
                raise ValidationError({
                    "cupo": f"Hay {inscritos} estudiantes matriculados; no puede reducir el cupo a {self.cupo}."
                })
            original = type(self).objects.filter(pk=self.pk).values("curso_id", "periodo_id").first()
            if original and inscritos and (
                original["curso_id"] != self.curso_id or
                original["periodo_id"] != self.periodo_id
            ):
                raise ValidationError(
                    "No se puede cambiar el curso ni el período de una sección con matrículas."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def inscritos(self):
        return self.matriculas.count()


# Modelo Matricula: inscripción de un estudiante en una sección
class Matricula(ModeloBase):

    # Estudiante que se matricula
    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.PROTECT,
        related_name="matriculas"
    )

    # Sección en la que se matricula
    seccion = models.ForeignKey(
        Seccion,
        on_delete=models.PROTECT,
        related_name="matriculas"
    )

    # Fecha de matrícula
    fecha = models.DateField(default=timezone.localdate)

    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        ordering = ["-fecha"]

        constraints = [
            models.UniqueConstraint(
                fields=["estudiante", "seccion"],
                name="matricula_unica"
            ),
        ]

    def __str__(self):
        return f"{self.estudiante} → {self.seccion}"

    def clean(self):
        # Si falta el estudiante o la sección, no continuamos.
        if not self.estudiante_id or not self.seccion_id:
            return

        # Verificar que el curso pertenezca a su carrera.
        if self.seccion.curso.carrera_id != self.estudiante.carrera_id:
            raise ValidationError(
                "El curso no pertenece a la carrera del estudiante."
            )

        # Contar las matrículas existentes en la sección.
        ocupados = self.seccion.matriculas.exclude(
            pk=self.pk
        ).count()

        # Comprobar que exista un cupo disponible.
        if ocupados >= self.seccion.cupo:
            raise ValidationError(
                f"La sección no tiene cupo ({self.seccion.cupo} estudiantes)."
            )


    def save(self, *args, **kwargs):
        # La validación también se aplica al guardar mediante scripts o Django Admin.
        self.full_clean()
        return super().save(*args, **kwargs)


# Modelo Nota: calificaciones de una matrícula
class Nota(ModeloBase):

    # Cada matrícula tendrá un registro de notas
    matricula = models.OneToOneField(
        Matricula,
        on_delete=models.PROTECT,
        related_name="nota"
    )

    # Tres calificaciones entre 0 y 100
    n1 = models.DecimalField(
        "Nota 1",
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=VALIDAR_NOTA
    )

    n2 = models.DecimalField(
        "Nota 2",
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=VALIDAR_NOTA
    )

    n3 = models.DecimalField(
        "Nota 3",
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=VALIDAR_NOTA
    )

    # Resultados calculados automáticamente
    promedio = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        editable=False
    )

    estado = models.CharField(
        max_length=10,
        choices=EstadoNota.choices,
        default=EstadoNota.REPROBADO,
        editable=False
    )

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"

    def __str__(self):
        return f"{self.matricula.estudiante} · {self.promedio} ({self.get_estado_display()})"

    def save(self, *args, **kwargs):
        # Calcular el promedio de las tres notas
        self.promedio = (
            (self.n1 + self.n2 + self.n3) / 3
        ).quantize(Decimal("0.01"))

        # Determinar si el estudiante aprueba
        self.estado = (
            EstadoNota.APROBADO
            if self.promedio >= NOTA_MINIMA_APROBACION
            else EstadoNota.REPROBADO
        )

        # Revalidar incluso si la escritura no proviene de un ModelForm.
        self.full_clean()
        super().save(*args, **kwargs)
