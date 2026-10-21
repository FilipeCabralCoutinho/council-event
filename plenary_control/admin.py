from django.contrib import admin
from plenary_control.models import Participante
from plenary_control.services import PlenaryService


@admin.action(description="Exportar Participantes para Excel")
def action_export_excel(modeladmin, request, queryset):
    #logger.info(f"User {request.user} triggered the export of {queryset.count()} participants to Excel via Admin.")
    return PlenaryService.export_participants_to_excel(queryset)


@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('id_participante', 'nome', 'distrito', 'igreja', 'funcao', 'no_plenario',)
    search_fields = ('id_participante', 'nome',)
    list_filter = ('distrito', 'igreja', 'funcao', 'no_plenario',)
    readonly_fields = ('id_participante',)
    actions = [action_export_excel]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def changelist_view(self, request, extra_context=None):
            # Intercepta a submissão da action antes da validação de checkboxes do Django
            if request.method == "POST" and request.POST.get("action") == "action_export_excel":
                # 1. Obtém o ChangeList com os filtros/busca aplicados na tela
                cl = self.get_changelist_instance(request)
                
                # 2. Pega o queryset filtrado (respeitando busca e list_filter ativos)
                queryset = cl.get_queryset(request)
                
                # 3. Executa a exportação diretamente
                return action_export_excel(self, request, queryset)

            return super().changelist_view(request, extra_context=extra_context)
