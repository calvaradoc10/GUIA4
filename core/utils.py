
from io import BytesIO

from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from django.template.loader import render_to_string
from xhtml2pdf import pisa


def generar_excel(encabezados, filas, nombre_archivo="reporte.xlsx"):
    # Crear el libro de Excel
    libro = Workbook()
    hoja = libro.active
    hoja.title = "Reporte Académico"

    # Agregar los encabezados
    hoja.append(encabezados)

    # Aplicar formato a los encabezados
    for celda in hoja[1]:
        celda.font = Font(
            bold=True,
            color="FFFFFF"
        )
        celda.fill = PatternFill(
            start_color="1F4E78",
            end_color="1F4E78",
            fill_type="solid"
        )
        celda.alignment = Alignment(
            horizontal="center"
        )

    # Agregar los registros
    for fila in filas:
        valores = []

        for valor in fila:
            if valor is None:
                valor = ""
            elif isinstance(valor, str) and valor.lstrip().startswith(
                ("=", "+", "-", "@")
            ):
                # Evitar interpretar texto como fórmula
                valor = "'" + valor

            valores.append(valor)

        hoja.append(valores)

    # Ajustar el ancho de las columnas
    for columna in hoja.columns:
        numero = columna[0].column
        letra = get_column_letter(numero)

        ancho = max(
            len(str(celda.value or ""))
            for celda in columna
        )

        hoja.column_dimensions[letra].width = min(
            ancho + 3, 50
        )

    # Guardar el archivo en memoria
    archivo = BytesIO()
    libro.save(archivo)
    archivo.seek(0)

    # Preparar la descarga
    respuesta = HttpResponse(
        archivo.getvalue(),
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )

    respuesta["Content-Disposition"] = (
        f'attachment; filename="{nombre_archivo}"'
    )

    return respuesta


def generar_pdf(
    nombre_plantilla,
    contexto,
    nombre_archivo="reporte.pdf"
):
    # Convertir la plantilla HTML en contenido
    html = render_to_string(
        nombre_plantilla,
        contexto
    )

    # Preparar la respuesta como documento PDF
    respuesta = HttpResponse(
        content_type="application/pdf"
    )

    respuesta["Content-Disposition"] = (
        f'attachment; filename="{nombre_archivo}"'
    )

    # Generar el documento PDF
    resultado = pisa.CreatePDF(
        src=html,
        dest=respuesta,
        encoding="UTF-8"
    )

    # Comprobar si ocurrió algún error
    if resultado.err:
        return HttpResponse(
            "No se pudo generar el documento PDF.",
            status=500
        )
    return respuesta