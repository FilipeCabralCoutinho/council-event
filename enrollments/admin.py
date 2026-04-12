from django.contrib import admin
from .models import Inscricoes, Distrito, Igreja, Pagamento, Parcela, Painel
from .services import Services
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import redirect

admin.site.register([Distrito, Igreja])

@admin.action(description="Exportar Inscrições Selecionadas para Excel")
def action_export_excel(modeladmin, request, queryset):
    return Services.export_to_excel(queryset)

@admin.register(Inscricoes)
class IncricoesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cpf', 'status_pagamento', 'ver_pagamento')
    exclude = ('consent_given', 'ip_address', 'last_email')
    readonly_fields = ('id',)
    actions = [action_export_excel]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for field in ['distrito', 'igreja']:
            if field in form.base_fields:
                form.base_fields[field].widget.can_add_related = False
                form.base_fields[field].widget.can_change_related = False
                form.base_fields[field].widget.can_delete_related = False
                form.base_fields[field].widget.can_view_related = False
        return form

    def ver_pagamento(self, obj):
        if hasattr(obj, 'pagamento'):
            url = reverse('admin:enrollments_pagamento_change', args=[obj.pagamento.id])
            return format_html('<a href="{}">Ver pagamento</a>', url)
        return "Sem pagamento"

    ver_pagamento.short_description = "Pagamento"

class ParcelaInline(admin.TabularInline):
    model = Parcela
    extra = 0

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    inlines = [ParcelaInline]

@admin.register(Painel)
class PainelAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        return redirect('enrollments:dashboard')

    def has_add_permission(self, request):
        return False  # Remove o botão "Adicionar" ao lado do menu

    def has_view_permission(self, request, obj=None):
        return True  # Garante que qualquer membro da equipe consiga ver o menu

    def has_module_permission(self, request):
        return True  # Garante acesso ao módulo no painel para qualquer membro da equipe