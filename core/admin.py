from django.contrib import admin
from .models import Relatorio, RelatorioImagem, DestinatarioEmail

admin.site.register(Relatorio)
admin.site.register(RelatorioImagem)
admin.site.register(DestinatarioEmail)
