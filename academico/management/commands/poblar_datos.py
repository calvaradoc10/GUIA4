
# Comando para generar datos de prueba del Sistema Académico
from decimal import Decimal
from datetime import date
from django.core.management.base import BaseCommand

from academico.models import (Universidad, Facultad, Carrera,Semestre,Periodo,Curso,Profesor,Estudiante,Seccion,Jornada,Matricula,Nota)


class Command(BaseCommand):
    help = "Genera datos de prueba del Sistema Académico"

    def handle(self, *args, **options):

        # Crear la Universidad de Guayaquil
        ug, creada = Universidad.objects.get_or_create(
            nombre="Universidad de Guayaquil",
            defaults={
                "siglas": "UG",
                "ciudad": "Guayaquil"
            }
        )

        # Crear la Universidad Estatal de Milagro
        unemi, creada = Universidad.objects.get_or_create(
            nombre="Universidad Estatal de Milagro",
            defaults={
                "siglas": "UNEMI",
                "ciudad": "Milagro"
            }
        )

        # Crear la primera facultad de la UG
        facultad1, creada = Facultad.objects.get_or_create(
            universidad=ug,
            nombre="Facultad de Ciencias Matemáticas y Físicas",
            defaults={
                "decano": ""
            }
        )

        # Crear la segunda facultad de la UG
        facultad2, creada = Facultad.objects.get_or_create(
            universidad=ug,
            nombre="Facultad de Ciencias Administrativas",
            defaults={
                "decano": ""
            }
        )

        # Crear la tercera facultad de UNEMI
        facultad3, creada = Facultad.objects.get_or_create(
            universidad=unemi,
            nombre="Facultad de Ciencias e Ingeniería",
            defaults={
                "decano": ""
            }
        )

        # Primera carrera: Ingeniería en Software
        carrera1, creada = Carrera.objects.get_or_create(
            codigo="SOF",
            defaults={
                "facultad": facultad1,
                "nombre": "Ingeniería en Software",
                "duracion_semestres": 8
            }
        )

        # Segunda carrera: Administración de Empresas
        carrera2, creada = Carrera.objects.get_or_create(
            codigo="ADM",
            defaults={
                "facultad": facultad2,
                "nombre": "Administración de Empresas",
                "duracion_semestres": 8
            }
        )

        # Tercera carrera: Tecnologías de la Información
        carrera3, creada = Carrera.objects.get_or_create(
            codigo="TIC",
            defaults={
                "facultad": facultad3,
                "nombre": "Ingeniería en Tecnologías de la Información",
                "duracion_semestres": 8
            }
        )

        # Crear el primer semestre
        semestre1, creada = Semestre.objects.get_or_create(
            numero=1,
            defaults={
                "nombre": "Primer semestre"
            }
        )

        # Crear el segundo semestre
        semestre2, creada = Semestre.objects.get_or_create(
            numero=2,
            defaults={
                "nombre": "Segundo semestre"
            }
        )

        # Crear el periodo académico activo
        periodo, creada = Periodo.objects.get_or_create(
            nombre="2026-2",
            defaults={
                "fecha_inicio": date(2026, 10, 1),
                "fecha_fin": date(2027, 2, 28),
                "activo": True
            }
        )

        # Cursos de Ingeniería en Software
        curso1, creado = Curso.objects.get_or_create(
            codigo="SOF-101",
            defaults={
                "nombre": "Fundamentos de Programación",
                "carrera": carrera1,
                "semestre": semestre1,
                "creditos": 3
            }
        )

        curso2, creado = Curso.objects.get_or_create(
            codigo="SOF-201",
            defaults={
                "nombre": "Programación Orientada a Objetos",
                "carrera": carrera1,
                "semestre": semestre2,
                "creditos": 3
            }
        )

        # Cursos de Administración de Empresas
        curso3, creado = Curso.objects.get_or_create(
            codigo="ADM-101",
            defaults={
                "nombre": "Fundamentos de Administración",
                "carrera": carrera2,
                "semestre": semestre1,
                "creditos": 3
            }
        )

        curso4, creado = Curso.objects.get_or_create(
            codigo="ADM-201",
            defaults={
                "nombre": "Contabilidad General",
                "carrera": carrera2,
                "semestre": semestre2,
                "creditos": 3
            }
        )

        # Cursos de Tecnologías de la Información
        curso5, creado = Curso.objects.get_or_create(
            codigo="TIC-101",
            defaults={
                "nombre": "Introducción a las TIC",
                "carrera": carrera3,
                "semestre": semestre1,
                "creditos": 3
            }
        )

        curso6, creado = Curso.objects.get_or_create(
            codigo="TIC-201",
            defaults={
                "nombre": "Redes de Computadoras",
                "carrera": carrera3,
                "semestre": semestre2,
                "creditos": 3
            }
        )

        # Profesor de Ingeniería en Software
        profesor1, creado = Profesor.objects.get_or_create(
            cedula="9000000001",
            defaults={
                "nombres": "Carlos Andrés",
                "apellidos": "Mendoza Vera",
                "email": "carlos.mendoza@example.com",
                "titulo": "Magíster en Ingeniería de Software"
            }
        )

        # Profesora de Administración
        profesor2, creado = Profesor.objects.get_or_create(
            cedula="9000000002",
            defaults={
                "nombres": "María Fernanda",
                "apellidos": "López Castro",
                "email": "maria.lopez@example.com",
                "titulo": "Magíster en Administración"
            }
        )

        # Profesor de Tecnologías de la Información
        profesor3, creado = Profesor.objects.get_or_create(
            cedula="9000000003",
            defaults={
                "nombres": "José Luis",
                "apellidos": "Zambrano Torres",
                "email": "jose.zambrano@example.com",
                "titulo": "Magíster en Redes y Telecomunicaciones"
            }
        )

        # Crear 15 estudiantes ficticios de prueba
        datos_estudiantes = [
            # Ingeniería en Software
            ("9000000101", "Andrés", "Mendoza Vera", carrera1),
            ("9000000102", "Daniel", "Zambrano López", carrera1),
            ("9000000103", "María", "Castro Torres", carrera1),
            ("9000000104", "José", "Vera Sánchez", carrera1),
            ("9000000105", "Gabriela", "Morales Díaz", carrera1),
            ("9000000106", "Carlos", "Pérez Gómez", carrera1),
            ("9000000107", "Valeria", "Ortega Ruiz", carrera1),
            ("9000000108", "Luis", "Ramírez Castro", carrera1),
            ("9000000109", "Diana", "Cedeño Mora", carrera1),
            ("9000000110", "Miguel", "López Paredes", carrera1),

            # Administración de Empresas
            ("9000000111", "Fernanda", "González Vera", carrera2),
            ("9000000112", "Pedro", "Salazar Mendoza", carrera2),
            ("9000000113", "Andrea", "Torres León", carrera2),

            # Tecnologías de la Información
            ("9000000114", "Sofía", "Vargas Castro", carrera3),
            ("9000000115", "Jorge", "Cabrera Pérez", carrera3),
        ]

        # Registrar cada estudiante sin duplicarlo
        creados_estudiantes = 0

        for cedula, nombres, apellidos, carrera in datos_estudiantes:
            estudiante, creado = Estudiante.objects.get_or_create(
                cedula=cedula,
                defaults={
                    "nombres": nombres,
                    "apellidos": apellidos,
                    "carrera": carrera,
                    "email": f"estudiante{cedula}@example.com",
                    "telefono": ""
                }
            )

            if creado:
                creados_estudiantes += 1

        self.stdout.write(
            f"Estudiantes nuevos: {creados_estudiantes}"
        )

        self.stdout.write(
            f"Total de estudiantes: {Estudiante.objects.count()}"
        )

        # Sección 1: Fundamentos de Programación
        seccion1, creada = Seccion.objects.get_or_create(
            curso=curso1,
            periodo=periodo,
            paralelo="A",
            jornada=Jornada.DIURNA,
            defaults={
                "profesor": profesor1,
                "cupo": 30
            }
        )

        # Sección 2: Programación Orientada a Objetos
        seccion2, creada = Seccion.objects.get_or_create(
            curso=curso2,
            periodo=periodo,
            paralelo="A",
            jornada=Jornada.NOCTURNA,
            defaults={
                "profesor": profesor1,
                "cupo": 30
            }
        )

        # Sección 3: Fundamentos de Administración
        seccion3, creada = Seccion.objects.get_or_create(
            curso=curso3,
            periodo=periodo,
            paralelo="A",
            jornada=Jornada.DIURNA,
            defaults={
                "profesor": profesor2,
                "cupo": 30
            }
        )

        # Sección 4: Introducción a las TIC
        seccion4, creada = Seccion.objects.get_or_create(
            curso=curso5,
            periodo=periodo,
            paralelo="A",
            jornada=Jornada.NOCTURNA,
            defaults={
                "profesor": profesor3,
                "cupo": 30
            }
        )

        # Crear las 25 matrículas de prueba
        plan_matriculas = [
            (seccion1, datos_estudiantes[0:10]),
            (seccion2, datos_estudiantes[0:10]),
            (seccion3, datos_estudiantes[10:13]),
            (seccion4, datos_estudiantes[13:15])
        ]

        nuevas_matriculas = 0

        for seccion, grupo in plan_matriculas:
            for cedula, nombres, apellidos, carrera in grupo:

                # Buscar al estudiante por su cédula
                estudiante = Estudiante.objects.get(
                    cedula=cedula
                )

                # Evitar matrículas duplicadas
                if Matricula.objects.filter(
                    estudiante=estudiante,
                    seccion=seccion
                ).exists():
                    continue

                # Preparar la matrícula
                matricula = Matricula(
                    estudiante=estudiante,
                    seccion=seccion
                )

                # Validar carrera, cupos y demás reglas
                matricula.full_clean()

                # Guardar en SQLite
                matricula.save()

                nuevas_matriculas += 1

        self.stdout.write(
            f"Matrículas nuevas: {nuevas_matriculas}"
        )

        self.stdout.write(
            f"Total de matrículas: {Matricula.objects.count()}"
        )

        # Crear las 25 notas de prueba
        calificaciones = [
            ("90.00", "85.00", "80.00"),
            ("60.00", "55.00", "65.00"),
            ("75.00", "80.00", "85.00"),
            ("40.00", "50.00", "60.00"),
            ("70.00", "75.00", "80.00")
        ]

        nuevas_notas = 0
        contador = 0

        for seccion, grupo in plan_matriculas:
            for cedula, nombres, apellidos, carrera in grupo:

                # Buscar la matrícula correspondiente
                matricula = Matricula.objects.get(
                    estudiante__cedula=cedula,
                    seccion=seccion
                )

                # Elegir las tres notas de prueba
                n1, n2, n3 = calificaciones[
                    contador % len(calificaciones)
                ]

                # Crear las notas sin duplicarlas
                nota, creada = Nota.objects.get_or_create(
                    matricula=matricula,
                    defaults={
                        "n1": Decimal(n1),
                        "n2": Decimal(n2),
                        "n3": Decimal(n3)
                    }
                )

                if creada:
                    nuevas_notas += 1

                contador += 1

        self.stdout.write(
            f"Notas nuevas: {nuevas_notas}"
        )

        self.stdout.write(
            f"Total de notas: {Nota.objects.count()}"
        )

        self.stdout.write(
            self.style.SUCCESS("Universidades, facultades, carreras, semestres, periodo, cursos, profesores, estudiantes,secciones,Matriculas y Notas registrados correctamente")
        )
