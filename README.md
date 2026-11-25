# Sistema Académico — Django

Proyecto universitario con **11 módulos CRUD** (Universidad, Facultad, Carrera, Semestre, Período, Curso, Profesor, Estudiante, Sección, Matrícula y Nota), panel de inicio, login propio y reportes Excel/PDF.

## Instalación (Windows / PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abre `http://127.0.0.1:8000/` (redirige al login si no hay sesión). **No hay usuario ni contraseña predeterminados**. Si ya tienes una base de datos local y un superusuario, conserva tu archivo `db.sqlite3` y ejecuta `migrate`; no crees una nueva cuenta si no es necesario. Para datos ficticios de demostración, opcionalmente ejecuta `python manage.py poblar_datos` en una base de datos de pruebas (NO sobre registros académicos reales).

## Cambios de la revisión

- Login propio en `/login/` (vistas basadas en clases), acceso autenticado a los 11 CRUD y logout vía `POST` protegido por CSRF.
- Barra compartida **Volver al inicio / Cerrar sesión** en las 33 pantallas CRUD y el dashboard.
- **Notas protegidas**: una matrícula con notas no puede eliminarse accidentalmente (`PROTECT`).
- Validaciones de matrícula: carrera, cupo y duplicado; además no reducir cupos por debajo de inscripciones ni cambiar curso/período de una sección con matrículas.
- Validación de formato de cédula y fecha de nacimiento en el formulario de estudiantes. (No se aplicó el dígito verificador ecuatoriano porque la carga inicial usa cédulas ficticias.)
- Evita ofrecer matrículas ya calificadas al crear una Nota; las tres notas deben estar entre 0 y 100. El promedio y estado se calculan en el modelo.
- Ajustes de `LANGUAGE_CODE`, `TIME_ZONE`, `MEDIA_URL`, codificación UTF-8 de dependencias y configuración por variables de entorno.

## Seguridad y despliegue

**El archivo original incluía una `SECRET_KEY` de desarrollo en el código, que pudo haber sido subida a GitHub. Debes cambiar esa clave antes de publicar en producción.** No se ha copiado a esta revisión.

- Desarrollo local: `DJANGO_DEBUG=1` (predeterminado), usa una clave local temporal y permite `localhost` / `127.0.0.1`.
- Producción: configurar `DJANGO_DEBUG=0`, `DJANGO_SECRET_KEY` aleatoria robusta, y `DJANGO_ALLOWED_HOSTS` con los dominios autorizados. Implementar HTTPS, servidor WSGI/ASGI, almacenamiento de estáticos/media y protección operativa antes de desplegar.
- SQLite, imágenes cargadas, entornos virtuales y `.env` no se incluyen en este ZIP para proteger datos privados. Si usas una base de datos existente, **haz copia de seguridad antes de migrar**.
- Cambio de base de datos: ejecutar `python manage.py migrate` para aplicar `academico/migrations/0002_nota_proteger_matricula.py`.

## Verificaciones

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test academico
```

Para generar un usuario adicional:

```powershell
python manage.py createsuperuser
```

Los usuarios no administradores pueden iniciar sesión en el sistema y acceder a CRUD según la política de este proyecto escolar; no se han definido roles granulares. Si se necesita un modelo de permisos por profesor/secretaría/administrador, debe acordarse e implementarse antes de usar datos reales.
