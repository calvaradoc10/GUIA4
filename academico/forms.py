
from django import forms
from django.db.models import Q
from django.utils import timezone
from .models import Estudiante, Carrera , Universidad,Facultad,Semestre,Periodo,Curso,Profesor,Seccion,Matricula,Nota


class EstudianteForm(forms.ModelForm):

    class Meta:
        model = Estudiante

        fields = [
            "cedula",
            "nombres",
            "apellidos",
            "email",
            "telefono",
            "fecha_nacimiento",
            "carrera",
            "foto",
        ]

        widgets = {
            "cedula": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "nombres": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "apellidos": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
            "telefono": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "fecha_nacimiento": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                },
                format="%Y-%m-%d"
            ),
            "carrera": forms.Select(
                attrs={"class": "form-select"}
            ),
            "foto": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
        }


    def clean_cedula(self):
        return _validar_cedula_formato(self.cleaned_data["cedula"])

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get("fecha_nacimiento")
        if fecha and fecha > timezone.localdate():
            raise forms.ValidationError("La fecha de nacimiento no puede ser futura.")
        return fecha


# Validaciones complementarias de datos personales.
# (Las cédulas de prueba cargadas por la guía son números ficticios;
# por ello se comprueba el formato y no el dígito verificador ecuatoriano.)

def _validar_cedula_formato(cedula):
    cedula = cedula.strip()
    if len(cedula) != 10 or not cedula.isdigit():
        raise forms.ValidationError("La cédula debe contener exactamente 10 dígitos.")
    return cedula


# ==========================================
# FORMULARIO DE CARRERAS
# ==========================================

class CarreraForm(forms.ModelForm):

    class Meta:
        model = Carrera

        fields = [
            "facultad",
            "codigo",
            "nombre",
            "duracion_semestres",
        ]

        widgets = {
            "facultad": forms.Select(
                attrs={"class": "form-select"}
            ),

            "codigo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Código de la carrera"
                }
            ),

            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre de la carrera"
                }
            ),

            "duracion_semestres": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1"
                }
            ),
        }

    def clean_duracion_semestres(self):
        duracion = self.cleaned_data["duracion_semestres"]

        if duracion is not None and duracion < 1:
            raise forms.ValidationError(
                "La duración debe ser de al menos un semestre."
            )

        return duracion


# ==========================================
# FORMULARIO DE UNIVERSIDADES
# ==========================================

class UniversidadForm(forms.ModelForm):

    class Meta:
        model = Universidad

        fields = [
            "nombre",
            "siglas",
            "ciudad",
            "logo",
        ]

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre de la universidad"
                }
            ),

            "siglas": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: UNEMI"
                }
            ),

            "ciudad": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ciudad de la universidad"
                }
            ),

            "logo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*"
                }
            ),
        }

    def clean_siglas(self):
        siglas = self.cleaned_data["siglas"]
        return siglas.strip().upper()


# ==========================================
# FORMULARIO DE FACULTADES
# ==========================================

class FacultadForm(forms.ModelForm):

    class Meta:
        model = Facultad

        fields = [
            "universidad",
            "nombre",
            "decano",
        ]

        widgets = {
            "universidad": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre de la facultad"
                }
            ),

            "decano": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del decano (opcional)"
                }
            ),
        }

        labels = {
            "universidad": "Universidad",
            "nombre": "Nombre de la facultad",
            "decano": "Decano",
        }


# ==========================================
# FORMULARIO DE SEMESTRES
# ==========================================

class SemestreForm(forms.ModelForm):

    class Meta:
        model = Semestre

        fields = [
            "numero",
            "nombre",
        ]

        widgets = {
            "numero": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: 1",
                    "min": 1,
                    "max": 12,
                    "step": 1,
                }
            ),

            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: Primer semestre",
                    "maxlength": 30,
                }
            ),
        }

        labels = {
            "numero": "Número de semestre",
            "nombre": "Nombre del semestre",
        }

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()

        if not nombre:
            raise forms.ValidationError(
                "Ingrese el nombre del semestre."
            )

        return nombre

# ==========================================
# FORMULARIO DE PERIODOS ACADEMICOS
# ==========================================

class PeriodoForm(forms.ModelForm):

    class Meta:
        model = Periodo

        fields = [
            "nombre",
            "fecha_inicio",
            "fecha_fin",
            "activo",
        ]

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: 2026-1",
                    "maxlength": 20,
                }
            ),

            "fecha_inicio": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "fecha_fin": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "activo": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

        labels = {
            "nombre": "Nombre del período",
            "fecha_inicio": "Fecha de inicio",
            "fecha_fin": "Fecha de finalización",
            "activo": "Período activo",
        }

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()

        if not nombre:
            raise forms.ValidationError(
                "Ingrese el nombre del período académico."
            )

        return nombre
    
    
# ==========================================
# FORMULARIO DE CURSOS
# ==========================================

class CursoForm(forms.ModelForm):

    class Meta:
        model = Curso

        fields = [
            "carrera",
            "semestre",
            "codigo",
            "nombre",
            "creditos",
        ]

        widgets = {
            "carrera": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "semestre": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "codigo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: SOF101",
                    "maxlength": 12,
                }
            ),

            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: Programación Orientada a Objetos",
                }
            ),

            "creditos": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: 3",
                    "min": 1,
                    "step": 1,
                }
            ),
        }

        labels = {
            "carrera": "Carrera universitaria",
            "semestre": "Semestre académico",
            "codigo": "Código del curso",
            "nombre": "Nombre de la asignatura",
            "creditos": "Número de créditos",
        }

    def clean_codigo(self):
        codigo = self.cleaned_data["codigo"]
        return codigo.strip().upper()

    def clean_creditos(self):
        creditos = self.cleaned_data["creditos"]

        if creditos < 1:
            raise forms.ValidationError(
                "Los créditos deben ser mayores que cero."
            )

        return creditos


# ==========================================
# FORMULARIO DE PROFESORES
# ==========================================

class ProfesorForm(forms.ModelForm):

    class Meta:
        model = Profesor

        fields = [
            "cedula",
            "nombres",
            "apellidos",
            "email",
            "titulo",
        ]

        widgets = {
            "cedula": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingrese la cédula de 10 dígitos",
                    "maxlength": 10,
                    "inputmode": "numeric",
                }
            ),

            "nombres": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombres del profesor",
                }
            ),

            "apellidos": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Apellidos del profesor",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: profesor@universidad.edu.ec",
                }
            ),

            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: Magíster en Ingeniería de Software",
                }
            ),
        }

        labels = {
            "cedula": "Número de cédula",
            "nombres": "Nombres",
            "apellidos": "Apellidos",
            "email": "Correo electrónico",
            "titulo": "Título académico",
        }

    # Validación de cédula
    def clean_cedula(self):
        cedula = self.cleaned_data["cedula"].strip()

        if not cedula.isdigit() or len(cedula) != 10:
            raise forms.ValidationError(
                "La cédula debe contener exactamente 10 dígitos."
            )

        return cedula

    # Normalizar nombres
    def clean_nombres(self):
        nombres = self.cleaned_data["nombres"].strip()

        if not nombres:
            raise forms.ValidationError(
                "Ingrese los nombres del profesor."
            )

        return nombres

    # Normalizar apellidos
    def clean_apellidos(self):
        apellidos = self.cleaned_data["apellidos"].strip()

        if not apellidos:
            raise forms.ValidationError(
                "Ingrese los apellidos del profesor."
            )

        return apellidos


# ==========================================
# FORMULARIO DE SECCIONES ACADEMICAS
# ==========================================

class SeccionForm(forms.ModelForm):

    class Meta:
        model = Seccion

        fields = [
            "curso",
            "periodo",
            "profesor",
            "paralelo",
            "jornada",
            "cupo",
        ]

        widgets = {

            "curso": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "periodo": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "profesor": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "paralelo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: A",
                    "maxlength": 2,
                }
            ),

            "jornada": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "cupo": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: 30",
                    "min": 1,
                    "step": 1,
                }
            ),
        }

        labels = {
            "curso": "Curso académico",
            "periodo": "Período académico",
            "profesor": "Profesor responsable",
            "paralelo": "Paralelo",
            "jornada": "Jornada académica",
            "cupo": "Cupo de estudiantes",
        }

    # ======================================
    # VALIDAR PARALELO
    # ======================================

    def clean_paralelo(self):
        paralelo = self.cleaned_data["paralelo"].strip().upper()

        if not paralelo:
            raise forms.ValidationError(
                "Debe ingresar el paralelo."
            )

        if len(paralelo) > 2:
            raise forms.ValidationError(
                "El paralelo no puede superar 2 caracteres."
            )

        return paralelo

    # ======================================
    # VALIDAR CUPO
    # ======================================

    def clean_cupo(self):
        cupo = self.cleaned_data["cupo"]

        if cupo < 1:
            raise forms.ValidationError(
                "El cupo debe ser mayor que cero."
            )

        return cupo


# ==========================================
# FORMULARIO DE MATRICULAS ACADEMICAS
# ==========================================

class MatriculaForm(forms.ModelForm):

    class Meta:
        model = Matricula

        fields = [
            "estudiante",
            "seccion",
            "fecha",
        ]

        widgets = {
            "estudiante": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "seccion": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "fecha": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }

        labels = {
            "estudiante": "Estudiante",
            "seccion": "Sección académica",
            "fecha": "Fecha de matrícula",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Mostrar estudiantes ordenados alfabéticamente
        self.fields["estudiante"].queryset = (
            Estudiante.objects.all().order_by(
                "apellidos",
                "nombres"
            )
        )

        # Mostrar las secciones organizadas
        self.fields["seccion"].queryset = (
            Seccion.objects.select_related(
                "curso",
                "periodo"
            ).order_by(
                "-periodo__fecha_inicio",
                "curso__codigo",
                "paralelo"
            )
        )


# ==========================================
# FORMULARIO DE NOTAS ACADEMICAS
# ==========================================

class NotaForm(forms.ModelForm):

    class Meta:
        model = Nota

        fields = [
            "matricula",
            "n1",
            "n2",
            "n3",
        ]

        widgets = {
            "matricula": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "n1": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: 85.00",
                    "min": "0",
                    "max": "100",
                    "step": "0.01",
                }
            ),

            "n2": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: 90.00",
                    "min": "0",
                    "max": "100",
                    "step": "0.01",
                }
            ),

            "n3": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ejemplo: 80.00",
                    "min": "0",
                    "max": "100",
                    "step": "0.01",
                }
            ),
        }

        labels = {
            "matricula": "Matrícula del estudiante",
            "n1": "Primera calificación",
            "n2": "Segunda calificación",
            "n3": "Tercera calificación",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ordenar las matrículas por estudiante
        # Mostrar solo matrículas sin nota, manteniendo la actual en edición.
        permitidas = Q(nota__isnull=True)
        if self.instance.pk and self.instance.matricula_id:
            permitidas |= Q(pk=self.instance.matricula_id)
        self.fields["matricula"].queryset = (
            Matricula.objects.filter(permitidas).select_related(
                "estudiante", "seccion", "seccion__curso", "seccion__periodo"
            ).order_by("estudiante__apellidos", "estudiante__nombres")
        )
