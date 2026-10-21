from django.contrib import admin
from plenary_control.models import Participante

"""Criar export to excel e modificar essa action"""
"""@admin.action(description="Exportar Participantes Selecionados para Excel")
def action_export_excel(modeladmin, request, queryset):
    logger.info(f"User {request.user} triggered the export of {queryset.count()} enrollments to Excel via Admin.")
    return Services.export_to_excel(queryset)"""


@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('id_participante', 'nome', 'distrito', 'igreja', 'funcao', 'no_plenario',)
    search_fields = ('id_participante', 'nome',)
    list_filter = ('distrito', 'igreja', 'funcao', 'no_plenario',)
    readonly_fields = ('id_participante',)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
