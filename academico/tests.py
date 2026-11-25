"""Pruebas funcionales de autenticación, CRUD, integridad y reportes."""
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import EstudianteForm, MatriculaForm, NotaForm, SeccionForm, PeriodoForm, CursoForm
from .models import (
    Carrera, Curso, Estudiante, Facultad, Matricula, Nota,
    Periodo, Profesor, Seccion, Semestre, Universidad,
)


class SistemaAcademicoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = get_user_model().objects.create_user(
            username="operador_pruebas", password="PruebaSegura#2026"
        )
        cls.universidad = Universidad.objects.create(
            nombre="Universidad de Pruebas", siglas="UP", ciudad="Milagro"
        )
        cls.facultad = Facultad.objects.create(
            universidad=cls.universidad, nombre="Facultad de Tecnología"
        )
        cls.carrera = Carrera.objects.create(
            facultad=cls.facultad, codigo="TIC", nombre="Tecnologías de Información", duracion_semestres=8
        )
        cls.carrera_otra = Carrera.objects.create(
            facultad=cls.facultad, codigo="ADM", nombre="Administración", duracion_semestres=8
        )
        cls.semestre = Semestre.objects.create(numero=1, nombre="Primer semestre")
        cls.periodo = Periodo.objects.create(
            nombre="2026-B", fecha_inicio=date(2026, 9, 1), fecha_fin=date(2027, 2, 28)
        )
        cls.curso = Curso.objects.create(
            carrera=cls.carrera, semestre=cls.semestre,
            codigo="TIC101", nombre="Fundamentos de programación", creditos=3
        )
        cls.curso_otra = Curso.objects.create(
            carrera=cls.carrera_otra, semestre=cls.semestre,
            codigo="ADM101", nombre="Gestión empresarial", creditos=3
        )
        cls.profesor = Profesor.objects.create(
            cedula="0912345678", nombres="Ana", apellidos="Docente"
        )
        cls.estudiante = Estudiante.objects.create(
            cedula="0901234567", nombres="Prueba", apellidos="Uno", carrera=cls.carrera
        )
        cls.estudiante_segundo = Estudiante.objects.create(
            cedula="0901234568", nombres="Prueba", apellidos="Dos", carrera=cls.carrera
        )
        cls.seccion = Seccion.objects.create(
            curso=cls.curso, periodo=cls.periodo, profesor=cls.profesor,
            paralelo="A", jornada="diurna", cupo=2
        )
        cls.seccion_otra = Seccion.objects.create(
            curso=cls.curso_otra, periodo=cls.periodo, profesor=cls.profesor,
            paralelo="A", jornada="diurna", cupo=2
        )
        cls.matricula = Matricula.objects.create(
            estudiante=cls.estudiante, seccion=cls.seccion
        )
        cls.nota = Nota.objects.create(
            matricula=cls.matricula,
            n1=Decimal("85"), n2=Decimal("90"), n3=Decimal("80")
        )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.modulos = {
            "universidad": "universidad",
            "facultad": "facultad",
            "carrera": "carrera",
            "semestre": "semestre",
            "periodo": "periodo",
            "curso": "curso",
            "profesor": "profesor",
            "estudiante": "estudiante",
            "seccion": "seccion",
            "matricula": "matricula",
            "nota": "nota",
        }

    def ejemplar(self, nombre):
        return {
            "universidad": self.universidad,
            "facultad": self.facultad,
            "carrera": self.carrera,
            "semestre": self.semestre,
            "periodo": self.periodo,
            "curso": self.curso,
            "profesor": self.profesor,
            "estudiante": self.estudiante,
            "seccion": self.seccion,
            "matricula": self.matricula,
            "nota": self.nota,
        }[nombre]

    def test_login_y_logout_por_post(self):
        login = reverse("login")
        self.assertEqual(self.client.get(login).status_code, 200)
        self.assertContains(self.client.get(login), "Sistema Académico")
        respuesta_invalida = self.client.post(login, {
            "username": "operador_pruebas", "password": "no-es-la-contrasena"
        })
        self.assertEqual(respuesta_invalida.status_code, 200)
        respuesta = self.client.post(login, {
            "username": "operador_pruebas", "password": "PruebaSegura#2026"
        })
        self.assertRedirects(respuesta, reverse("inicio"))
        self.assertEqual(self.client.get(reverse("inicio")).status_code, 200)
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.assertRedirects(self.client.post(reverse("logout")), reverse("login"))
        self.assertEqual(self.client.get(reverse("inicio")).status_code, 302)

    def test_las_44_rutas_crud_requieren_login(self):
        for modulo in self.modulos:
            pk = self.ejemplar(modulo).pk
            for operacion, kwargs in [
                ("lista", {}), ("crear", {}), ("editar", {"pk": pk}),
                ("eliminar", {"pk": pk}),
            ]:
                with self.subTest(modulo=modulo, operacion=operacion):
                    url = reverse(f"academico:{modulo}_{operacion}", kwargs=kwargs)
                    respuesta = self.client.get(url)
                    self.assertEqual(respuesta.status_code, 302)
                    self.assertIn(reverse("login"), respuesta.url)
        self.assertEqual(self.client.get(reverse("inicio")).status_code, 302)
        url = reverse("academico:estudiante_lista")
        self.assertEqual(self.client.get(url + "?exportar=excel").status_code, 302)
        self.assertEqual(self.client.get(url + "?exportar=pdf").status_code, 302)

    def test_las_44_vistas_crud_y_menu_renderizan(self):
        self.client.force_login(self.usuario)
        self.assertContains(self.client.get(reverse("inicio")), "Cerrar sesión")
        for modulo in self.modulos:
            pk = self.ejemplar(modulo).pk
            for operacion, kwargs in [
                ("lista", {}), ("crear", {}), ("editar", {"pk": pk}),
                ("eliminar", {"pk": pk}),
            ]:
                with self.subTest(modulo=modulo, operacion=operacion):
                    url = reverse(f"academico:{modulo}_{operacion}", kwargs=kwargs)
                    respuesta = self.client.get(url)
                    self.assertEqual(respuesta.status_code, 200)
                    self.assertContains(respuesta, "Volver al inicio")
                    self.assertContains(respuesta, "Cerrar sesión")

    def test_excel_y_pdf_de_los_11_modulos(self):
        self.client.force_login(self.usuario)
        for modulo in self.modulos:
            url = reverse(f"academico:{modulo}_lista")
            with self.subTest(modulo=modulo, formato="excel"):
                respuesta = self.client.get(url, {"exportar": "excel"})
                self.assertEqual(respuesta.status_code, 200)
                self.assertIn("spreadsheetml", respuesta["Content-Type"])
                self.assertTrue(respuesta.content.startswith(b"PK"))
            with self.subTest(modulo=modulo, formato="pdf"):
                respuesta = self.client.get(url, {"exportar": "pdf"})
                self.assertEqual(respuesta.status_code, 200)
                self.assertEqual(respuesta["Content-Type"], "application/pdf")
                self.assertTrue(respuesta.content.startswith(b"%PDF"))

    def test_matricula_duplicada_se_rechaza(self):
        form = MatriculaForm(data={
            "estudiante": self.estudiante.pk, "seccion": self.seccion.pk,
            "fecha": "2026-11-25"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    def test_matricula_en_carrera_distinta_se_rechaza(self):
        form = MatriculaForm(data={
            "estudiante": self.estudiante_segundo.pk, "seccion": self.seccion_otra.pk,
            "fecha": "2026-11-25"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    def test_cupo_lleno_impide_inscripcion(self):
        # Simular sección llena sin pasar por save(), que impide la reducción de cupo.
        Seccion.objects.filter(pk=self.seccion.pk).update(cupo=1)
        form = MatriculaForm(data={
            "estudiante": self.estudiante_segundo.pk, "seccion": self.seccion.pk,
            "fecha": "2026-11-25"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    def test_editar_seccion_no_puede_reducir_cupo_bajo_inscritos(self):
        form = SeccionForm(data={
            "curso": self.curso.pk, "periodo": self.periodo.pk,
            "profesor": self.profesor.pk, "paralelo": "A",
            "jornada": "diurna", "cupo": 0
        }, instance=self.seccion)
        self.assertFalse(form.is_valid())

    def test_seccion_con_matriculas_no_puede_cambiar_curso(self):
        form = SeccionForm(data={
            "curso": self.curso_otra.pk, "periodo": self.periodo.pk,
            "profesor": self.profesor.pk, "paralelo": "A",
            "jornada": "diurna", "cupo": 2
        }, instance=self.seccion)
        self.assertFalse(form.is_valid())

    def test_no_se_borran_notas_al_intentar_eliminar_matricula(self):
        self.client.force_login(self.usuario)
        url = reverse("academico:matricula_eliminar", kwargs={"pk": self.matricula.pk})
        respuesta = self.client.post(url)
        self.assertRedirects(respuesta, reverse("academico:matricula_lista"))
        self.assertTrue(Matricula.objects.filter(pk=self.matricula.pk).exists())
        self.assertTrue(Nota.objects.filter(pk=self.nota.pk).exists())

    def test_nota_solo_admite_valores_de_cero_a_cien(self):
        for n1 in ("-1", "100.01"):
            with self.subTest(valor=n1):
                form = NotaForm(data={
                    "matricula": self.matricula.pk,
                    "n1": n1, "n2": "70", "n3": "70",
                }, instance=self.nota)
                self.assertFalse(form.is_valid())
                self.assertIn("n1", form.errors)

    def test_nota_calcula_promedio_y_estado_en_edicion(self):
        self.client.force_login(self.usuario)
        url = reverse("academico:nota_editar", kwargs={"pk": self.nota.pk})
        respuesta = self.client.post(url, {
            "matricula": self.matricula.pk,
            "n1": "60", "n2": "65", "n3": "70",
        })
        self.assertRedirects(respuesta, reverse("academico:nota_lista"))
        self.nota.refresh_from_db()
        self.assertEqual(self.nota.promedio, Decimal("65.00"))
        self.assertEqual(self.nota.estado, "reprobado")

    def test_crear_nota_no_ofrece_matriculas_ya_calificadas(self):
        form = NotaForm()
        self.assertNotIn(self.matricula.pk, list(form.fields["matricula"].queryset.values_list("pk",flat=True)))
        form_edicion = NotaForm(instance=self.nota)
        self.assertIn(self.matricula.pk, list(form_edicion.fields["matricula"].queryset.values_list("pk",flat=True)))

    def test_estudiante_cedula_y_fecha_nacimiento(self):
        form = EstudianteForm(data={
            "cedula": "123", "nombres": "Luis", "apellidos": "Pérez",
            "carrera": self.carrera.pk, "fecha_nacimiento": (date.today() + timedelta(days=2)).isoformat()
        })
        self.assertFalse(form.is_valid())
        self.assertIn("cedula",form.errors)
        self.assertIn("fecha_nacimiento",form.errors)

    def test_periodo_y_creditos_invalidos(self):
        pform = PeriodoForm(data={
            "nombre": "Prueba-2", "fecha_inicio": "2026-12-31", "fecha_fin": "2026-01-01", "activo": "on"
        })
        self.assertFalse(pform.is_valid())
        self.assertIn("fecha_fin",pform.errors)
        cform = CursoForm(data={
            "carrera": self.carrera.pk, "semestre": self.semestre.pk,
            "codigo": "TIC202", "nombre": "Curso nuevo", "creditos": 0
        })
        self.assertFalse(cform.is_valid())
        self.assertIn("creditos",cform.errors)

    def test_estudiante_con_matriculas_no_puede_eliminarse(self):
        self.client.force_login(self.usuario)
        url = reverse("academico:estudiante_eliminar", kwargs={"pk": self.estudiante.pk})
        respuesta = self.client.post(url)
        self.assertRedirects(respuesta, reverse("academico:estudiante_lista"))
        self.assertTrue(Estudiante.objects.filter(pk=self.estudiante.pk).exists())

    def test_crear_editar_y_eliminar_los_11_crud(self):
        """Todos los formularios usan POST real sin alterar la base de datos del usuario."""
        self.client.force_login(self.usuario)
        casos = {
            "universidad": (
                Universidad,
                {"nombre":"Instituto Nuevo", "siglas":"IN", "ciudad":"Guayaquil"},
                "ciudad", "Quito",
            ),
            "facultad": (
                Facultad,
                {"universidad":self.universidad.pk, "nombre":"Ciencias Exactas", "decano":""},
                "decano", "Decano Ejemplo",
            ),
            "carrera": (
                Carrera,
                {"facultad":self.facultad.pk, "codigo":"SOFT", "nombre":"Ingeniería Software", "duracion_semestres":8},
                "nombre", "Software e Innovación",
            ),
            "semestre": (
                Semestre,
                {"numero":2, "nombre":"Segundo semestre"},
                "nombre", "Nivel segundo",
            ),
            "periodo": (
                Periodo,
                {"nombre":"2027-A", "fecha_inicio":"2027-03-01", "fecha_fin":"2027-08-31", "activo":"on"},
                "nombre", "2027-1",
            ),
            "curso": (
                Curso,
                {"carrera":self.carrera.pk, "semestre":self.semestre.pk, "codigo":"TIC999", "nombre":"Curso Ejemplo", "creditos":3},
                "nombre", "Curso Ejemplo Actualizado",
            ),
            "profesor": (
                Profesor,
                {"cedula":"0912345679", "nombres":"Mario", "apellidos":"Docente", "email":"mario@ejemplo.com", "titulo":"Magíster"},
                "titulo", "Doctor",
            ),
            "estudiante": (
                Estudiante,
                {"cedula":"0901234569", "nombres":"María", "apellidos":"Alumno", "email":"maria@ejemplo.com", "telefono":"", "fecha_nacimiento":"2000-01-01", "carrera":self.carrera.pk},
                "apellidos", "Alumno Prueba",
            ),
            "seccion": (
                Seccion,
                {"curso":self.curso.pk, "periodo":self.periodo.pk, "profesor":self.profesor.pk, "paralelo":"B", "jornada":"nocturna", "cupo":20},
                "cupo", 18,
            ),
            "matricula": (
                Matricula,
                {"estudiante":self.estudiante_segundo.pk, "seccion":self.seccion.pk, "fecha":"2026-11-25"},
                "fecha", "2026-11-26",
            ),
        }
        casos["nota"] = (
            Nota,
            {"matricula": None, "n1":"75", "n2":"80", "n3":"85"},
            "n1", "90",
        )
        for modulo, (modelo, datos, campo_a_editar, valor_nuevo) in casos.items():
            if modulo == "nota":
                # Se crea después de terminar el CRUD Matrícula para no duplicarla.
                matricula_disponible = Matricula.objects.create(
                    estudiante=self.estudiante_segundo, seccion=self.seccion
                )
                datos["matricula"] = matricula_disponible.pk
            with self.subTest(modulo=modulo, operacion="crear"):
                cuenta = modelo.objects.count()
                respuesta = self.client.post(reverse(f"academico:{modulo}_crear"), datos)
                self.assertEqual(respuesta.status_code, 302, respuesta.content[:800])
                self.assertEqual(modelo.objects.count(), cuenta + 1)
                creado = modelo.objects.latest("pk")
            with self.subTest(modulo=modulo, operacion="editar"):
                datos_edicion = {**datos, campo_a_editar: valor_nuevo}
                respuesta = self.client.post(
                    reverse(f"academico:{modulo}_editar", kwargs={"pk": creado.pk}),
                    datos_edicion,
                )
                self.assertEqual(respuesta.status_code, 302, respuesta.content[:800])
                creado.refresh_from_db()
                valor = getattr(creado, campo_a_editar)
                if campo_a_editar == "fecha":
                    self.assertEqual(valor, date.fromisoformat(valor_nuevo))
                elif campo_a_editar == "cupo":
                    self.assertEqual(valor, valor_nuevo)
                elif campo_a_editar == "n1":
                    self.assertEqual(valor, Decimal(valor_nuevo))
                else:
                    self.assertEqual(valor, valor_nuevo)
            with self.subTest(modulo=modulo, operacion="eliminar"):
                respuesta = self.client.post(
                    reverse(f"academico:{modulo}_eliminar", kwargs={"pk": creado.pk})
                )
                self.assertEqual(respuesta.status_code, 302)
                self.assertFalse(modelo.objects.filter(pk=creado.pk).exists())
