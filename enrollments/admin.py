from django.contrib import admin
from .models import Inscricoes, Distrito, Igreja, Pagamento, Parcela
from .services import Services
from django.utils.html import format_html
from django.urls import reverse

admin.site.register([Distrito, Igreja])

@admin.action(description="Exportar Inscrições Selecionadas para Excel")
def action_export_excel(modeladmin, request, queryset):
    return Services.export_to_excel(queryset)

@admin.register(Inscricoes)
class IncricoesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cpf', 'status_pagamento', 'ver_pagamento')
    actions = [action_export_excel]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
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