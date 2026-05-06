from django.contrib import admin, messages
from .models import Inscricoes, Distrito, Igreja, Pagamento, Parcela, Painel, EmailControl
from .services import Services
from .management.emails_controls import EmailReSender
from django.utils.html import format_html
from django.urls import reverse, path
from django.shortcuts import redirect
from .logging import logger

admin.site.register([Distrito, Igreja])

@admin.action(description="Exportar Inscrições Selecionadas para Excel")
def action_export_excel(modeladmin, request, queryset):
    logger.info(f"User {request.user} triggered the export of {queryset.count()} enrollments to Excel via Admin.")
    return Services.export_to_excel(queryset)

@admin.register(Inscricoes)
class IncricoesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cpf', 'status_pagamento', 'ver_pagamento', 'botao_enviar_email')
    search_fields = ('id', 'nome', 'cpf')
    list_filter = ('status_pagamento',)
    exclude = ('consent_given', 'ip_address', 'last_email')
    readonly_fields = ('id',)
    actions = [action_export_excel]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:inscricao_id>/enviar-email/',
                self.admin_site.admin_view(self.enviar_email_view),
                name='enrollments_inscricoes_enviar_email',
            ),
        ]
        return custom_urls + urls

    def botao_enviar_email(self, obj):
        try:
            url = reverse('admin:enrollments_inscricoes_enviar_email', args=[obj.id])
            return format_html('<a class="button" style="background-color: #417690; color: white; padding: 5px 10px; border-radius: 4px; font-weight: bold; text-decoration: none;" href="{}">Enviar E-mail Atualização Pagamento</a>', url)
        except Exception as e:
            return format_html('<span style="color: red;">Erro: {}</span>', str(e))
    botao_enviar_email.short_description = "Ação"

    def enviar_email_view(self, request, inscricao_id):
        try:
            inscricao = Inscricoes.objects.get(id=inscricao_id)
            service = Services()
            service.send_email(inscricao, email_type='update_payment_email')
            self.message_user(request, f"E-mail de atualização enviado com sucesso para {inscricao.nome}!", messages.SUCCESS)
        except Inscricoes.DoesNotExist:
            self.message_user(request, "Erro: Inscrição não encontrada.", level=messages.ERROR)
            
        return redirect('admin:enrollments_inscricoes_changelist')


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
        logger.info(f"User {request.user} accessed the Dashboard shortcut in Admin.")
        return redirect('enrollments:dashboard')

    def has_add_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


@admin.register(EmailControl)
class EmailControlAdmin(admin.ModelAdmin):
    list_display = ('enrollment_id', 'email_type', 'created_at', 'status')
    list_filter = ('status',)
    search_fields = ('enrollment_id',)
    change_list_template = "enrollments/emailcontrol_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('reenviar-emails/', self.admin_site.admin_view(self.reenviar_emails_view), name='emailcontrol_reenviar_emails'),
        ]
        return custom_urls + urls

    def reenviar_emails_view(self, request):
        from threading import Thread
        
        # Executa em uma thread separada para evitar Timeout na tela (já que há um time.sleep na rotina original)
        Thread(target=EmailReSender().resend_failed_emails).start()
        self.message_user(request, "Rotina de reenvio de e-mails iniciada em segundo plano!", messages.SUCCESS)
        return redirect('admin:enrollments_emailcontrol_changelist')
