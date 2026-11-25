# Informe de revisión — Sistema Académico

**Fecha:** 25 de noviembre de 2026  
**Origen:** ZIP entregado por el usuario, inspeccionado en una copia aislada.  
**Alcance:** Código de los 11 módulos CRUD, panel de inicio, autenticación, validación, navegación, migraciones y generación de reportes.

## Resumen ejecutivo

Se revisaron los 11 módulos: Universidad, Facultad, Carrera, Semestre, Período, Curso, Profesor, Estudiante, Sección, Matrícula y Nota. Se implementaron mejoras de seguridad, datos y experiencia de usuario **sin modificar la estructura principal de los CRUD**.

### Mejoras incorporadas

1. **Autenticación propia:** `/login/` con `LoginView` y formulario Bootstrap; `/logout/` con `LogoutView` que requiere POST y CSRF; `/` protegido y redirigido al login cuando corresponde. No se crean usuarios ni contraseñas predeterminados.
2. **Acceso restringido:** ahora los 44 endpoints CRUD (11 listados, 11 altas, 11 ediciones y 11 eliminaciones) requieren usuario autenticado. Se corrigió específicamente el listado público de Estudiantes.
3. **Navegación:** barra reutilizable con «Volver al inicio» y «Cerrar sesión» en las **33 pantallas CRUD**, más la barra de sesión en el panel principal.
4. **Protección de registros académicos:** `Nota.matricula` pasó de `CASCADE` a `PROTECT`. Se incluye migración `0002_nota_proteger_matricula.py`. Ahora una matrícula con notas **no se elimina accidentalmente**.
5. **Eliminación de estudiantes:** el CRUD captura `ProtectedError` si existen matrículas, evita un error 500 y notifica al usuario.
6. **Validaciones:** se mantienen reglas de matrícula (estudiante/sección únicos, carrera compatible y cupo); se impide reducir el cupo por debajo de inscripciones existentes, cambiar curso/período de secciones con matrículas o cambiar la carrera del estudiante dejando matrículas incompatibles. Las restricciones principales también se comprueban en guardados directos de modelos.
7. **Notas:** el formulario de creación muestra solo matrículas sin nota; las tres notas se validan entre 0 y 100, y el modelo guarda promedio y estado calculados.
8. **Estudiantes:** cédula de exactamente diez dígitos y fecha de nacimiento no futura. No se exige dígito verificador ecuatoriano porque los datos iniciales del ejercicio usan identificaciones ficticias.
9. **Configuración:** zona horaria America/Guayaquil, idioma español de Ecuador, rutas `MEDIA_URL` y `MEDIA_ROOT`, ajustes de autenticación y clave de producción desde variable de entorno. El archivo `requirements.txt` se convirtió de UTF-16 a UTF-8.
10. **Instrucciones:** README con instalación, migración, datos de demostración y seguridad.

### Verificaciones ejecutadas

| Verificación | Resultado |
|---|---|
| `python manage.py check` | Correcto; 0 problemas |
| `python manage.py makemigrations --check --dry-run` | Correcto; sin cambios pendientes |
| Suite automatizada `python manage.py test academico` | **17 pruebas superadas** |
| 44 rutas CRUD sin autenticación | Redirigen al login |
| 44 pantallas CRUD autenticadas | Responden correctamente y muestran navegación |
| 11 descargas Excel + 11 PDF | Generación satisfactoria en pruebas |
| Crear/editar/eliminar en cada módulo | **33 operaciones POST** verificadas en base de prueba |
| Matrículas duplicadas, carrera incompatible, cupo lleno | Rechazadas |
| Notas fuera de rango | Rechazadas |
| Cambio de cupo/curso con alumnos matriculados | Rechazado |
| Eliminación de matrícula con notas | Rechazada, sin pérdida de notas |
| Eliminación de estudiante con matrículas | Rechazada, sin error del servidor |
| Promedio y estado tras editar notas | Correctos |
| Migración en copia del SQLite entregado | Aplicada sin errores |
| Integridad SQLite y claves foráneas en copia | Correctas; sin claves foráneas rotas |
| Validación de registros existentes en copia | Sin problemas detectados |
| Carga inicial en base nueva | Correcta: 15 estudiantes, 25 matrículas y 25 notas |

Los PDF se generan correctamente; `xhtml2pdf` puede advertir que ignora la propiedad CSS `border-collapse`, lo cual es una limitación de estilo y no un error de generación.

### Datos y privacidad

Se utilizó **una copia temporal** de `db.sqlite3` para comprobar la migración y la integridad. Se eliminaron las bases de datos temporales. **El ZIP corregido no incluye** base de datos, respaldo, carpeta `.git`, `venv`, fotografías subidas ni archivos privados. Conserva esos elementos en tu computadora y no compartas contraseñas.

### Pendiente / limitaciones

- Las pruebas se ejecutaron automáticamente con Django 6.1.3 en un entorno de ejecución aislado. Aunque se comprobaron navegación, operaciones y reportes, conviene hacer la comprobación visual final en Chrome y Windows en tu equipo.
- El proyecto escolar permite que cualquier usuario **autenticado** utilice los CRUD; **no se han creado perfiles/roles granulares** para secretaría, docentes y estudiantes. No es un sistema listo para manejar registros reales en producción sin una política de permisos.
- El control de cupo es adecuado para operaciones ordinarias de la aplicación; no se ha verificado resistencia a matriculaciones simultáneas de alta concurrencia.
- Los archivos `media/` no se adjuntan. Si la base local tiene logotipos o fotos, conserva esa carpeta en tu instalación.
- La `SECRET_KEY` original estaba escrita directamente en el código fuente entregado; si fue publicada en GitHub, debe considerarse expuesta. La revisión elimina esa clave del código nuevo, pero **no borra el historial Git**. Para producción configura `DJANGO_SECRET_KEY` nueva, `DJANGO_DEBUG=0` y dominios autorizados.
- El archivo `requirements.txt` conserva versiones del entorno del usuario (incluida Django 6.1.3); son versiones concretas que deben instalarse en un Python compatible (el proyecto original utiliza Python 3.12).

## Cómo instalar esta revisión sin perder el progreso

1. **Crea un respaldo** de la carpeta original y en especial de `db.sqlite3` y `media/`.
2. **Extrae el ZIP en otra carpeta**. Copia su contenido de `sistema_academico/` a la carpeta original, reemplazando los archivos de código correspondientes. No borres tu carpeta `.git`, `venv`, `db.sqlite3` ni `media/` de la instalación local.
3. Desde VS Code, con el entorno `venv` activado, ejecuta:

   ```powershell
   python -m pip install -r requirements.txt
   python manage.py migrate
   python manage.py check
   python manage.py test academico
   python manage.py runserver
   ```

4. Abre `http://127.0.0.1:8000/`. Si no tienes sesión, se mostrará `http://127.0.0.1:8000/login/`. Inicia sesión con tu usuario ya existente. Si necesitas crear uno, usa `python manage.py createsuperuser`.
5. Comprueba visualmente los 11 botones del panel, los enlaces «Volver al inicio», el cierre de sesión y un reporte Excel/PDF.
6. Cuando verifiques todo, realiza `git status`, revisa que no se agregue información privada y registra un nuevo `git add` / `git commit` / `git push` en tu repositorio existente.

**Conclusión:** Correcciones implementadas y baterías automáticas completadas satisfactoriamente. No se afirma que el proyecto esté certificado para uso productivo ni que cubra todos los escenarios posibles.
