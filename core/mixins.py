
from django.views.generic import ListView
from core.utils import generar_excel, generar_pdf


class FiltroCamposMixin:
    filtro_form_class = None
    campos_disponibles = {}
    campos_por_defecto = []

    def get_filtro_form(self):
        if self.filtro_form_class is None:
            return None

        return self.filtro_form_class(self.request.GET)

    def filtrar(self, queryset, datos):
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()

        self.filtro_form = self.get_filtro_form()

        if self.filtro_form is not None:
            if self.filtro_form.is_valid():
                queryset = self.filtrar(
                    queryset,
                    self.filtro_form.cleaned_data
                )

        return queryset

    def get_campos_seleccionados(self):
        # Obtener las columnas solicitadas por el usuario
        campos = self.request.GET.getlist("campos")

        # Si no seleccionó columnas, usar las predeterminadas
        if not campos:
            campos = self.campos_por_defecto

        # Permitir únicamente columnas configuradas
        campos_validos = [
            campo for campo in campos
            if campo in self.campos_disponibles
        ]

        # Evitar que la tabla se quede sin columnas
        if not campos_validos:
            campos_validos = [
                campo for campo in self.campos_por_defecto
                if campo in self.campos_disponibles
            ]

        return campos_validos


    def obtener_valor_campo(self, objeto, campo):
        valor = objeto

        for parte in campo.split("__"):
            if valor is None:
                return ""

            valor = getattr(valor, parte, "")

        return str(valor) if valor is not None else ""

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        # Obtener las columnas seleccionadas
        campos = self.get_campos_seleccionados()

        # Preparar los encabezados de la tabla
        encabezados = [
            self.campos_disponibles[campo]
            for campo in campos
        ]

        # Preparar las filas con los registros
        filas = [
            [
                self.obtener_valor_campo(objeto, campo)
                for campo in campos
            ]
            for objeto in contexto["object_list"]
        ]

        # Enviar la información a la plantilla HTML
        contexto["filtro_form"] = getattr(
            self, "filtro_form", self.get_filtro_form()
        )
        contexto["campos_disponibles"] = self.campos_disponibles
        contexto["campos_seleccionados"] = campos
        contexto["encabezados"] = encabezados
        contexto["filas"] = filas

        return contexto

    def get(self, request, *args, **kwargs):
        # Comprobar si el usuario solicita un Excel
        if request.GET.get("exportar") == "excel":

            # Obtener los registros aplicando los filtros
            queryset = self.get_queryset()

            # Obtener las columnas seleccionadas
            campos = self.get_campos_seleccionados()

            # Preparar los encabezados
            encabezados = [
                self.campos_disponibles[campo]
                for campo in campos
            ]

            # Preparar los datos del reporte
            filas = [
                [
                    self.obtener_valor_campo(objeto, campo)
                    for campo in campos
                ]
                for objeto in queryset
            ]

            # Generar el archivo Excel
            return generar_excel(
                encabezados,
                filas,
                nombre_archivo="reporte_academico.xlsx"
            )

        # Exportar los registros a PDF
        if request.GET.get("exportar") == "pdf":

            # Obtener registros y aplicar filtros
            queryset = self.get_queryset()

            # Obtener las columnas seleccionadas
            campos = self.get_campos_seleccionados()

            # Preparar encabezados
            encabezados = [
                self.campos_disponibles[campo]
                for campo in campos
            ]

            # Preparar las filas del reporte
            filas = [
                [
                    self.obtener_valor_campo(objeto, campo)
                    for campo in campos
                ]
                for objeto in queryset
            ]

            # Información del documento
            contexto = {
                "titulo": getattr(
                    self,
                    "titulo_reporte",
                    "Reporte Académico"
                ),
                "encabezados": encabezados,
                "filas": filas
            }

            # Generar el PDF profesional
            return generar_pdf(
                "core/reporte_pdf.html",
                contexto,
                "reporte_academico.pdf"
            )

        # Si no solicita Excel, mostrar la página normal
        return super().get(request, *args, **kwargs)
