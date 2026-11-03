from django.contrib import admin
from plenary_control.models import Participante
from plenary_control.services import PlenaryService
from .logging import setup_logging
from .models import Plenario
from django.shortcuts import redirect
from django.contrib import admin, messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.template.response import TemplateResponse

logger = setup_logging()


@admin.action(description="Exportar Participantes para Excel")
def action_export_excel(modeladmin, request, queryset):
    logger.info(f"User {request.user} triggered the export of {queryset.count()} participants to Excel via Admin.")
    return PlenaryService.export_participants_to_excel(queryset)    


@admin.action(description="Marcar como fora do plenário")
def action_marcar_fora_plenario(modeladmin, request, queryset):

    # Primeira execução: exibe a confirmação
    if "confirmar" not in request.POST:
        context = {
            **modeladmin.admin_site.each_context(request),
            "title": "Confirmar ação",
            "queryset": queryset,
            "action_checkbox_name": ACTION_CHECKBOX_NAME,
            "opts": modeladmin.model._meta,
        }

        return TemplateResponse(
            request,
            "admin/confirmar_fora_plenario.html",
            context,
        )

    # Segunda execução: usuário confirmou
    quantidade = queryset.update(no_plenario=False)

    modeladmin.message_user(
        request,
        f"{quantidade} participante(s) marcado(s) como fora do plenário.",
        messages.SUCCESS,
    )


@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('id_participante', 'nome', 'distrito', 'igreja', 'funcao', 'no_plenario',)
    search_fields = ('id_participante', 'nome',)
    list_filter = ('distrito', 'igreja', 'funcao', 'no_plenario',)
    readonly_fields = ('id_participante',)
    actions = [action_export_excel, action_marcar_fora_plenario]

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


@admin.register(Plenario)
class PlenarioAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        logger.info(f"User {request.user} accessed the Plenary Control Page in Admin.")
        return redirect('plenary_control:dashboard')

    def has_add_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True